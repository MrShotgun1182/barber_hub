from unittest.mock import patch

from store import models as store_models
from store import services as store_services

from .test_cart_services import BaseStoreTestCase


def _FakeResponse(data, status_code=200):
    """پاسخ شبیه‌سازی‌شده requests.post"""

    class Resp:
        def __init__(self):
            self.status_code = status_code
            self._data = data

        def json(self):
            return self._data

    return Resp()


class PaymentVerifyTests(BaseStoreTestCase):
    """تست‌های تأیید پرداخت زرین‌پال: کد ۱۰۰/۱۰۱، callback تکراری، Status=NOK"""

    def _make_order_with_payment(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        order = store_services.CreateOrderService(self.customer)
        payment = store_services.CreatePaymentService(order)
        store_services.SetPaymentAuthorityService(payment, 'A0001')
        payment.refresh_from_db()
        return order, payment

    def test_verify_code_100_marks_verified_and_order_placed(self):
        order, payment = self._make_order_with_payment()
        with patch('store.services.zarinpal_verify_service.requests.post') as mock_post:
            mock_post.return_value = _FakeResponse(
                {'data': {'code': 100, 'ref_id': 12345}, 'errors': []}
            )
            result = store_services.ZarinPalVerifyService(payment, 'A0001')

        self.assertEqual(result['status'], 'verified')
        self.assertEqual(result['ref_id'], '12345')

        store_services.MarkPaymentVerifiedService(payment, 12345, 100)
        store_services.UpdateOrderStatusService(order, 'PLACED')
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.status, 'VERIFIED')
        self.assertEqual(payment.ref_id, '12345')
        self.assertEqual(order.status, 'PLACED')

    def test_verify_code_101_is_idempotent_replay(self):
        # کد ۱۰۱ یعنی تراکنش قبلاً تأیید شده؛ باید موفق تلقی شود
        order, payment = self._make_order_with_payment()
        with patch('store.services.zarinpal_verify_service.requests.post') as mock_post:
            mock_post.return_value = _FakeResponse(
                {'data': {'code': 101, 'ref_id': 12345}, 'errors': []}
            )
            result = store_services.ZarinPalVerifyService(payment, 'A0001')
        self.assertEqual(result['status'], 'verified')

    def test_duplicate_callback_does_not_verify_twice(self):
        # اکشن تأیید باید برای callback تکراری بدون تماس مجدد با درگاه، موفق برگردد
        from store import actions as store_actions

        order, payment = self._make_order_with_payment()
        with patch('store.services.zarinpal_verify_service.requests.post') as mock_post:
            mock_post.return_value = _FakeResponse(
                {'data': {'code': 100, 'ref_id': 999}, 'errors': []}
            )
            first = store_actions.VerifyPaymentAction('A0001', 'OK')
            self.assertEqual(first['status'], 'success')

            # callback تکراری: نباید دوباره به درگاه زده شود
            second = store_actions.VerifyPaymentAction('A0001', 'OK')
            self.assertEqual(second['status'], 'success')
            self.assertEqual(mock_post.call_count, 1)

        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.status, 'VERIFIED')
        self.assertEqual(order.status, 'PLACED')

    def test_failed_verify_keeps_order_pending_and_retry_possible(self):
        from store import actions as store_actions

        order, payment = self._make_order_with_payment()
        with patch('store.services.zarinpal_verify_service.requests.post') as mock_post:
            mock_post.return_value = _FakeResponse(
                {'data': {'code': -50, 'message': 'amount mismatch'}, 'errors': []}
            )
            result = store_actions.VerifyPaymentAction('A0001', 'OK')

        self.assertEqual(result['status'], 'error')
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.status, 'FAILED')
        self.assertEqual(order.status, 'PENDING_PAYMENT')

        # تلاش مجدد با پرداخت جدید ممکن است
        new_payment = store_services.CreatePaymentService(order)
        self.assertEqual(new_payment.status, 'INITIATED')
        self.assertNotEqual(new_payment.id, payment.id)

    def test_nok_status_cancels_payment(self):
        from store import actions as store_actions

        order, payment = self._make_order_with_payment()
        result = store_actions.VerifyPaymentAction('A0001', 'NOK')

        self.assertEqual(result['status'], 'error')
        payment.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(payment.status, 'CANCELLED')
        self.assertEqual(order.status, 'PENDING_PAYMENT')

    def test_request_success_returns_payment_url(self):
        order, payment = self._make_order_with_payment()
        with patch('store.services.zarinpal_request_service.requests.post') as mock_post:
            mock_post.return_value = _FakeResponse(
                {'data': {'code': 100, 'authority': 'A0002'}, 'errors': []}
            )
            result = store_services.ZarinPalRequestService(payment)
        self.assertEqual(result['authority'], 'A0002')
        self.assertIn('/pg/StartPay/A0002', result['payment_url'])

    def test_request_network_error_raises_persian(self):
        import requests as requests_lib

        order, payment = self._make_order_with_payment()
        with patch(
            'store.services.zarinpal_request_service.requests.post',
            side_effect=requests_lib.RequestException,
        ):
            with self.assertRaises(ValueError):
                store_services.ZarinPalRequestService(payment)

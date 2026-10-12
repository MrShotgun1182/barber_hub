from store import models as store_models
from store import services as store_services

from .test_cart_services import BaseStoreTestCase


class StatusTransitionTests(BaseStoreTestCase):
    """تست‌های گذار وضعیت سفارش: زنجیره مجاز، پرش غیرمجاز، تأثیر لغو بر پرداخت"""

    def _make_paid_order(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        order = store_services.CreateOrderService(self.customer)
        payment = store_services.CreatePaymentService(order)
        store_services.MarkPaymentVerifiedService(payment, ref_id='123', code=100)
        store_services.UpdateOrderStatusService(order, 'PLACED')
        return order, payment

    def test_legal_chain_to_delivered(self):
        order, _ = self._make_paid_order()
        for status in ('VIEWED', 'READY_FOR_PICKUP', 'DELIVERED'):
            store_services.UpdateOrderStatusService(order, status)
            order.refresh_from_db()
            self.assertEqual(order.status, status)

    def test_illegal_jump_rejected(self):
        order, _ = self._make_paid_order()
        # پرش مستقیم از «ثبت‌شده» به «تحویل‌شده» مجاز نیست
        with self.assertRaises(ValueError):
            store_services.UpdateOrderStatusService(order, 'DELIVERED')
        order.refresh_from_db()
        self.assertEqual(order.status, 'PLACED')

    def test_no_transition_out_of_delivered(self):
        order, _ = self._make_paid_order()
        for status in ('VIEWED', 'READY_FOR_PICKUP', 'DELIVERED'):
            store_services.UpdateOrderStatusService(order, status)
        with self.assertRaises(ValueError):
            store_services.UpdateOrderStatusService(order, 'CANCELLED')
        with self.assertRaises(ValueError):
            store_services.UpdateOrderStatusService(order, 'PLACED')

    def test_cancel_from_placed_allowed(self):
        order, _ = self._make_paid_order()
        store_services.UpdateOrderStatusService(order, 'CANCELLED')
        order.refresh_from_db()
        self.assertEqual(order.status, 'CANCELLED')

    def test_no_transition_out_of_cancelled(self):
        order, _ = self._make_paid_order()
        store_services.UpdateOrderStatusService(order, 'CANCELLED')
        with self.assertRaises(ValueError):
            store_services.UpdateOrderStatusService(order, 'PLACED')

    def test_cancel_does_not_touch_payment_status(self):
        # لغو سفارش پرداخت‌شده به معنی بازگشت وجه نیست؛ پرداخت «تأییدشده» می‌ماند
        order, payment = self._make_paid_order()
        store_services.UpdateOrderStatusService(order, 'CANCELLED')
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'VERIFIED')
        self.assertEqual(payment.ref_id, '123')

    def test_pending_payment_only_goes_to_cancelled(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        order = store_services.CreateOrderService(self.customer)
        with self.assertRaises(ValueError):
            store_services.UpdateOrderStatusService(order, 'VIEWED')
        store_services.UpdateOrderStatusService(order, 'CANCELLED')
        order.refresh_from_db()
        self.assertEqual(order.status, 'CANCELLED')

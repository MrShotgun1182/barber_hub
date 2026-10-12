from unittest.mock import patch

from store import actions as store_actions
from store import models as store_models
from store import services as store_services

from .test_cart_services import BaseStoreTestCase


class CheckoutFlowTests(BaseStoreTestCase):
    """تست‌های فلوی تسویه: نیاز به تأیید، ایجاد سفارش، بازپخش ایدمپوتنت"""

    def _seed_cart(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)

    def _make_order_with_payment(self):
        self._seed_cart()
        order = store_services.CreateOrderService(self.customer)
        payment = store_services.CreatePaymentService(order)
        store_services.SetPaymentAuthorityService(payment, 'A0001')
        payment.refresh_from_db()
        return order, payment

    def test_price_change_requires_confirmation(self):
        self._seed_cart()
        # قیمت بعد از افزودن به سبد تغییر می‌کند
        self.product.price = 200000
        self.product.save()

        result = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-1'
        )
        self.assertEqual(result['status'], 'needs_confirmation')
        self.assertEqual(result['changes'][0]['change_type'], 'price_changed')
        # سفارشی ثبت نشده است
        self.assertFalse(
            store_models.OrderModel.objects.filter(customer=self.customer).exists()
        )

    def test_confirm_changes_creates_order_with_new_price(self):
        self._seed_cart()
        self.product.price = 200000
        self.product.save()

        result = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-2', confirm_changes=True
        )
        self.assertEqual(result['status'], 'success')
        order = result['order']
        self.assertEqual(order.total_amount, 200000)
        # سبد پاک شده است
        self.assertEqual(self.customer.cart.items.count(), 0)

    def test_not_orderable_blocks_order(self):
        self._seed_cart()
        self.product.is_orderable = False
        self.product.save()

        result = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-3', confirm_changes=True
        )
        self.assertEqual(result['status'], 'error')
        self.assertFalse(
            store_models.OrderModel.objects.filter(customer=self.customer).exists()
        )

    def test_repeated_post_returns_same_order(self):
        self._seed_cart()
        first = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-4', confirm_changes=True
        )
        self.assertEqual(first['status'], 'success')

        # ثبت تکراری با همان کلید → همان سفارش، بدون سفارش جدید
        second = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-4', confirm_changes=True
        )
        self.assertEqual(second['status'], 'success')
        self.assertTrue(second['already_exists'])
        self.assertEqual(second['order'].id, first['order'].id)
        self.assertEqual(
            store_models.OrderModel.objects.filter(customer=self.customer).count(), 1
        )

    def test_no_changes_creates_order_directly(self):
        self._seed_cart()
        result = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-5'
        )
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['order'].total_amount, 100000)

    def test_empty_cart_fails(self):
        result = store_actions.SubmitCheckoutAction(
            self.user, idempotency_key='key-6'
        )
        self.assertEqual(result['status'], 'error')

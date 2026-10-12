from store import models as store_models
from store import services as store_services

from .test_cart_services import BaseStoreTestCase


class OrderServiceTests(BaseStoreTestCase):
    """تست‌های ثبت سفارش: اسنپ‌شات قیمت، مجموع، پاک شدن سبد، کلید ایدمپوتنسی"""

    def _seed_cart(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=2)

    def test_order_number_format(self):
        number = store_services.GenerateOrderNumberService()
        self.assertRegex(number, r'^BH-\d{8}-\d{6}$')

    def test_order_snapshots_live_prices(self):
        self._seed_cart()
        # قیمت بعد از افزودن به سبد تغییر می‌کند؛ سفارش باید قیمت تازه را ثبت کند
        self.product.price = 120000
        self.product.save()

        order = store_services.CreateOrderService(self.customer)
        item = order.items.first()
        self.assertEqual(item.unit_price, 120000)
        self.assertEqual(item.product_title, self.product.title)
        self.assertEqual(order.total_amount, 240000)

    def test_order_price_immutable_after_creation(self):
        self._seed_cart()
        order = store_services.CreateOrderService(self.customer)
        self.product.price = 999999
        self.product.save()
        self.product.refresh_from_db()
        order.refresh_from_db()
        item = order.items.first()
        self.assertEqual(item.unit_price, 100000)
        self.assertEqual(order.total_amount, 200000)

    def test_order_clears_cart(self):
        self._seed_cart()
        store_services.CreateOrderService(self.customer)
        self.assertEqual(self.customer.cart.items.count(), 0)

    def test_order_on_empty_cart_fails(self):
        with self.assertRaises(ValueError):
            store_services.CreateOrderService(self.customer)

    def test_idempotency_key_replay_returns_existing(self):
        self._seed_cart()
        order = store_services.CreateOrderService(
            self.customer, idempotency_key='test-key-123'
        )
        existing = store_services.GetOrderByIdempotencyKeyService('test-key-123')
        self.assertEqual(existing.id, order.id)

    def test_customer_scoped_order_queries(self):
        self._seed_cart()
        order = store_services.CreateOrderService(self.customer)
        orders = list(store_services.GetCustomerOrdersService(self.customer))
        self.assertEqual(len(orders), 1)
        detail = store_services.GetCustomerOrderDetailService(
            self.customer, order.id
        )
        self.assertEqual(detail['order'].id, order.id)

    def test_order_scope_rejects_other_customers(self):
        from django.contrib.auth import get_user_model
        from customers import models as customers_models

        self._seed_cart()
        order = store_services.CreateOrderService(self.customer)

        other_user = get_user_model().objects.create_user(
            username='09121111111', phone_number='09121111111', role='CUSTOMER'
        )
        other_customer = customers_models.CustomerModel.objects.create(user=other_user)
        with self.assertRaises(ValueError):
            store_services.GetCustomerOrderDetailService(other_customer, order.id)

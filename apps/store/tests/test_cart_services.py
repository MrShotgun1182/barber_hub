from django.contrib.auth import get_user_model
from django.test import TestCase

from customers import models as customers_models
from store import models as store_models
from store import services as store_services

UserModel = get_user_model()


class BaseStoreTestCase(TestCase):
    """کلاس پایه تست‌های فروشگاه: کاربر/مشتری/دسته/محصول نمونه می‌سازد"""

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='09120000000',
            phone_number='09120000000',
            role='CUSTOMER',
        )
        self.customer = customers_models.CustomerModel.objects.create(user=self.user)
        self.category = store_models.CategoryModel.objects.create(name='اصلاح')
        self.product = store_models.ProductModel.objects.create(
            title='وکس موی سر',
            price=100000,
            category=self.category,
            is_published=True,
            is_orderable=True,
        )


class CartServiceTests(BaseStoreTestCase):
    """تست‌های سبد خرید: افزودن، افزایش تعداد، حذف با صفر، جمع کل"""

    def test_add_to_cart_creates_item(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=2)
        cart = self.customer.cart
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_add_to_cart_same_product_increments(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        store_services.AddToCartService(self.customer, self.product.id, quantity=3)
        self.assertEqual(self.customer.cart.items.count(), 1)
        self.assertEqual(self.customer.cart.items.first().quantity, 4)

    def test_add_unpublished_product_fails(self):
        self.product.is_published = False
        self.product.save()
        with self.assertRaises(ValueError):
            store_services.AddToCartService(self.customer, self.product.id)
        self.assertFalse(hasattr(self.customer, 'cart') and self.customer.cart.items.exists())

    def test_add_not_orderable_product_fails(self):
        self.product.is_orderable = False
        self.product.save()
        with self.assertRaises(ValueError):
            store_services.AddToCartService(self.customer, self.product.id)

    def test_update_quantity_zero_removes_item(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=2)
        item_id = self.customer.cart.items.first().id
        result = store_services.UpdateCartItemService(self.customer, item_id, 0)
        self.assertIsNone(result)
        self.assertEqual(self.customer.cart.items.count(), 0)

    def test_update_negative_quantity_fails(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=2)
        item_id = self.customer.cart.items.first().id
        with self.assertRaises(ValueError):
            store_services.UpdateCartItemService(self.customer, item_id, -1)

    def test_cart_summary_total_uses_live_price(self):
        # قیمت روی سبد ذخیره نمی‌شود؛ همیشه قیمت لحظه‌ای محصول خوانده می‌شود
        store_services.AddToCartService(self.customer, self.product.id, quantity=3)
        self.product.price = 150000
        self.product.save()
        summary = store_services.GetCartSummaryService(self.customer)
        self.assertEqual(summary['total'], 450000)
        self.assertEqual(summary['items_count'], 1)

    def test_cart_persists_across_multiple_accesses(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        cart_id = self.customer.cart.id
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        self.assertEqual(self.customer.cart.id, cart_id)

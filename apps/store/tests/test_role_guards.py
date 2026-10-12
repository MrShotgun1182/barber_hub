from django.contrib.auth import get_user_model
from django.test import Client

from store import models as store_models
from store import services as store_services

from .test_cart_services import BaseStoreTestCase

UserModel = get_user_model()

# مسیرهای پنل مدیریت فروشگاه که باید فقط برای مدیر مجاز باشند
MANAGER_URLS = [
    '/store/manage/categories/',
    '/store/manage/categories/new/',
    '/store/manage/products/',
    '/store/manage/products/new/',
    '/store/manage/orders/',
]


class RoleGuardTests(BaseStoreTestCase):
    """تست‌های محافظت دسترسی: ناشناس و مشتری ریدایرکت؛ مدیر ۲۰۰"""

    def setUp(self):
        super().setUp()
        self.manager = UserModel.objects.create_user(
            username='09129999999',
            phone_number='09129999999',
            role='MANAGER',
        )
        self.client = Client()

    def test_anonymous_redirected_to_admin_login(self):
        for url in MANAGER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 302, f'آدرس {url} باید ریدایرکت شود'
            )
            self.assertIn('admin', response.url, f'آدرس {url} باید به ورود مدیر برود')

    def test_customer_redirected_to_admin_login(self):
        self.client.force_login(self.user)
        for url in MANAGER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 302, f'آدرس {url} باید برای مشتری ریدایرکت شود'
            )

    def test_manager_gets_200(self):
        self.client.force_login(self.manager)
        for url in MANAGER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200, f'آدرس {url} باید برای مدیر باز شود'
            )

    def test_customer_pages_require_login(self):
        # صفحات سبد و سفارش‌ها فقط برای مشتری لاگین‌شده
        for url in ['/store/cart/', '/store/orders/', '/store/checkout/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f'آدرس {url} باید ریدایرکت شود')

    def test_store_home_is_public(self):
        store_services.CreateCategoryService(name='لوسیون')
        self.product.is_published = True
        self.product.save()
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)

    def test_manager_order_detail_scoped(self):
        # مشتری لاگین‌شده به جزئیات سفارش خودش می‌رسد؛ مدیر هم به همه
        self.client.force_login(self.user)
        store_services.AddToCartService(self.customer, self.product.id, quantity=1)
        order = store_services.CreateOrderService(self.customer)
        response = self.client.get(f'/store/orders/{order.id}/')
        self.assertEqual(response.status_code, 200)

        # مشتری دیگر نباید به این سفارش دسترسی داشته باشد
        other = UserModel.objects.create_user(
            username='09128888888', phone_number='09128888888', role='CUSTOMER'
        )
        self.client.force_login(other)
        response = self.client.get(f'/store/orders/{order.id}/')
        self.assertEqual(response.status_code, 404)

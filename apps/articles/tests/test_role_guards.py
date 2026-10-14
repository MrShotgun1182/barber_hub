from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from articles import services as articles_services
from barbers import models as barbers_models

from .test_article_services import BaseArticleTestCase

UserModel = get_user_model()

# مسیرهای پنل آرایشگر که باید فقط برای آرایشگر مجاز باشند
BARBER_URLS = [
    '/barber/articles/',
    '/barber/articles/new/',
]

# مسیرهای پنل مدیریت مقالات و برچسب‌ها که باید فقط برای مدیر مجاز باشند
MANAGER_URLS = [
    '/admin_panel/articles/',
    '/admin_panel/articles/new/',
    '/admin_panel/tags/',
    '/admin_panel/tags/new/',
]


class RoleGuardTests(BaseArticleTestCase):
    """تست‌های محافظت دسترسی: ناشناس/مشتری ریدایرکت؛ آرایشگر و مدیر مجاز"""

    def setUp(self):
        super().setUp()
        self.customer = UserModel.objects.create_user(
            username='09128888888',
            phone_number='09128888888',
            role='CUSTOMER',
        )
        self.client = Client()

    def test_public_article_list_is_public(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_public_article_detail_404_for_unpublished(self):
        article = self._create_article()
        response = self.client.get(f'/articles/{article.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_public_article_detail_shows_published(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)
        response = self.client.get(f'/articles/{article.slug}/')
        self.assertEqual(response.status_code, 200)

        # بازدید مقاله باید یک بار شمرده شود
        article.refresh_from_db()
        self.assertEqual(article.views_count, 1)

    def test_anonymous_redirected_from_barber_panel(self):
        for url in BARBER_URLS:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f'آدرس {url} باید ریدایرکت شود')

    def test_customer_redirected_from_barber_panel(self):
        self.client.force_login(self.customer)
        for url in BARBER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 302, f'آدرس {url} باید برای مشتری ریدایرکت شود'
            )
            self.assertIn('login', response.url, f'آدرس {url} باید به ورود برود')

    def test_barber_gets_200_on_own_panel(self):
        self.client.force_login(self.barber_user)
        for url in BARBER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200, f'آدرس {url} باید برای آرایشگر باز شود'
            )

    def test_barber_editing_others_article_forbidden(self):
        other_barber = UserModel.objects.create_user(
            username='09127777777', phone_number='09127777777', role='BARBER'
        )
        barbers_models.BarberModel.objects.create(user=other_barber)
        article = self._create_article()

        self.client.force_login(other_barber)
        response = self.client.get(f'/barber/articles/{article.id}/edit/')
        self.assertEqual(response.status_code, 403)

    def test_anonymous_redirected_from_manager_panels(self):
        for url in MANAGER_URLS:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f'آدرس {url} باید ریدایرکت شود')
            self.assertIn('admin', response.url, f'آدرس {url} باید به ورود مدیر برود')

    def test_barber_redirected_from_manager_panels(self):
        self.client.force_login(self.barber_user)
        for url in MANAGER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 302, f'آدرس {url} باید برای آرایشگر ریدایرکت شود'
            )
            self.assertIn('admin', response.url, f'آدرس {url} باید به ورود مدیر برود')

    def test_manager_gets_200_on_own_panels(self):
        self.client.force_login(self.manager)
        for url in MANAGER_URLS:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200, f'آدرس {url} باید برای مدیر باز شود'
            )

    def test_barber_cannot_toggle_featured(self):
        article = self._create_article()
        self.client.force_login(self.barber_user)
        response = self.client.post(
            f'/admin_panel/articles/{article.id}/featured/'
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('admin', response.url)

        article.refresh_from_db()
        self.assertFalse(article.is_featured)

    def test_barber_cannot_moderate(self):
        article = self._create_article()
        self.client.force_login(self.barber_user)
        response = self.client.post(
            f'/admin_panel/articles/{article.id}/moderate/',
            {'action': 'publish'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('admin', response.url)

        article.refresh_from_db()
        self.assertEqual(article.status, 'PENDING')

    def test_manager_publish_via_post(self):
        article = self._create_article()
        self.client.force_login(self.manager)
        response = self.client.post(
            f'/admin_panel/articles/{article.id}/moderate/',
            {'action': 'publish'},
        )
        self.assertEqual(response.status_code, 302)

        article.refresh_from_db()
        self.assertEqual(article.status, 'PUBLISHED')

    def test_manager_reject_via_post_stores_reason(self):
        article = self._create_article()
        self.client.force_login(self.manager)
        self.client.post(
            f'/admin_panel/articles/{article.id}/moderate/',
            {'action': 'reject', 'reason': 'محتوای نامناسب'},
        )
        article.refresh_from_db()
        self.assertEqual(article.status, 'REJECTED')
        self.assertEqual(article.rejection_reason, 'محتوای نامناسب')

    def test_moderation_requires_post(self):
        article = self._create_article()
        self.client.force_login(self.manager)
        response = self.client.get(f'/admin_panel/articles/{article.id}/moderate/')
        self.assertEqual(response.status_code, 405)

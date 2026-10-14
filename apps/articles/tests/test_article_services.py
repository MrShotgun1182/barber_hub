from django.contrib.auth import get_user_model
from django.test import TestCase

from articles import models as articles_models
from articles import services as articles_services
from barbers import models as barbers_models
from tags import services as tags_services

UserModel = get_user_model()


def _make_image(name='cover.png'):
    """ساخت فایل تصویر معتبر برای فیلدهای ImageField در تست‌ها"""
    # یک PNG یک‌پیکسلی معتبر
    from io import BytesIO

    from PIL import Image
    from django.core.files.uploadedfile import SimpleUploadedFile

    buffer = BytesIO()
    Image.new('RGB', (1, 1), color=(120, 150, 100)).save(buffer, format='PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


class BaseArticleTestCase(TestCase):
    """کلاس پایه تست‌های مقاله: آرایشگر، مدیر و برچسب نمونه می‌سازد"""

    def setUp(self):
        self.barber_user = UserModel.objects.create_user(
            username='09120000000',
            phone_number='09120000000',
            role='BARBER',
        )
        self.barber = barbers_models.BarberModel.objects.create(user=self.barber_user)
        self.manager = UserModel.objects.create_user(
            username='09129999999',
            phone_number='09129999999',
            role='MANAGER',
        )
        self.tag = tags_services.CreateTagService('اصلاح مو')

    def _create_article(self, **overrides):
        """مقاله نمونه با پیش‌فرض‌های معمول (نویسنده آرایشگر، در انتظار تایید)"""
        defaults = dict(
            author=self.barber_user,
            title='راهنمای مراقبت از ریش',
            content='پاراگراف اول\n\nپاراگراف دوم',
            cover_image=_make_image(),
            tag_ids=[self.tag.id],
        )
        defaults.update(overrides)
        return articles_services.CreateArticleService(**defaults)


class CreateArticleServiceTests(BaseArticleTestCase):
    """تست‌های ساخت مقاله: وضعیت اولیه، انتشار مستقیم و اعتبارسنجی"""

    def test_barber_create_goes_to_pending(self):
        article = self._create_article()
        self.assertEqual(article.status, 'PENDING')
        self.assertIsNone(article.published_at)
        self.assertEqual(article.views_count, 0)

    def test_manager_direct_publish(self):
        article = self._create_article(
            author=self.manager,
            title='مقاله مدیر',
            publish=True,
            is_featured=True,
        )
        self.assertEqual(article.status, 'PUBLISHED')
        self.assertIsNotNone(article.published_at)
        self.assertTrue(article.is_featured)

    def test_barber_direct_publish_fails(self):
        with self.assertRaises(ValueError):
            self._create_article(publish=True)

    def test_missing_title_fails(self):
        with self.assertRaises(ValueError):
            self._create_article(title='   ')

    def test_missing_content_fails(self):
        with self.assertRaises(ValueError):
            self._create_article(content='')

    def test_missing_cover_fails(self):
        with self.assertRaises(ValueError):
            self._create_article(cover_image=None)

    def test_invalid_tag_fails(self):
        with self.assertRaises(ValueError):
            self._create_article(tag_ids=[self.tag.id, 999])

    def test_gallery_images_with_sort_order(self):
        article = self._create_article(
            gallery_files=[_make_image('g1.png'), _make_image('g2.png')],
        )
        self.assertEqual(article.images.count(), 2)
        self.assertEqual(
            list(article.images.values_list('sort_order', flat=True)), [0, 1]
        )

    def test_persian_slug_from_title(self):
        article = self._create_article()
        self.assertEqual(article.slug, 'راهنمای-مراقبت-از-ریش')

    def test_duplicate_title_gets_suffix(self):
        first = self._create_article()
        second = self._create_article(
            title='راهنمای مراقبت از ریش نسخه دوم',
        )
        # عنوان متفاوت است ولی اسلاگ پایه مشترکی شامل می‌شود؛ یکتا بودن کلید است
        self.assertNotEqual(first.slug, second.slug)


class UpdateArticleServiceTests(BaseArticleTestCase):
    """تست‌های ویرایش: بازگشت به صف بازبینی، اسلاگ و مالکیت"""

    def test_barber_edit_resets_to_pending_and_clears_reason(self):
        article = self._create_article()
        articles_services.RejectArticleService(article.id, 'محتوای نامناسب')

        updated = articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title=article.title,
            content='محتوای اصلاح‌شده',
        )
        self.assertEqual(updated.status, 'PENDING')
        self.assertIsNone(updated.rejection_reason)

    def test_slug_regenerated_only_on_title_change(self):
        article = self._create_article()
        original_slug = article.slug

        same_title = articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title=article.title,
            content='محتوای جدید',
        )
        self.assertEqual(same_title.slug, original_slug)

        renamed = articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title='عنوان جدید مقاله',
            content='محتوای جدید',
        )
        self.assertEqual(renamed.slug, 'عنوان-جدید-مقاله')

    def test_gallery_appended_after_existing(self):
        article = self._create_article(
            gallery_files=[_make_image('g1.png')],
        )
        articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title=article.title,
            content=article.content,
            gallery_files=[_make_image('g2.png'), _make_image('g3.png')],
        )
        self.assertEqual(article.images.count(), 3)
        self.assertEqual(
            list(article.images.values_list('sort_order', flat=True)), [0, 1, 2]
        )

    def test_non_owner_edit_fails(self):
        article = self._create_article()
        other_barber = UserModel.objects.create_user(
            username='09121111111', phone_number='09121111111', role='BARBER'
        )
        with self.assertRaises(ValueError):
            articles_services.UpdateArticleService(
                article_id=article.id,
                editor=other_barber,
                title=article.title,
                content='محتوای مزاحم',
            )

    def test_manager_can_edit_any_article(self):
        article = self._create_article()
        updated = articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.manager,
            title=article.title,
            content='ویرایش توسط مدیر',
        )
        self.assertEqual(updated.content, 'ویرایش توسط مدیر')

    def test_manager_publish_on_update_keeps_first_published_at(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)
        article.refresh_from_db()
        first_published_at = article.published_at

        updated = articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.manager,
            title=article.title,
            content='ویرایش مدیر',
            publish=True,
        )
        self.assertEqual(updated.status, 'PUBLISHED')
        self.assertEqual(updated.published_at, first_published_at)


class ModerationServiceTests(BaseArticleTestCase):
    """تست‌های چرخه بازبینی: انتشار، رد، بایگانی و ویژه"""

    def test_publish_pending_article(self):
        article = self._create_article()
        published = articles_services.PublishArticleService(article.id)
        self.assertEqual(published.status, 'PUBLISHED')
        self.assertIsNotNone(published.published_at)

    def test_publish_non_pending_fails(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)
        with self.assertRaises(ValueError):
            articles_services.PublishArticleService(article.id)

    def test_first_publish_semantics_keeps_original_date(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)
        article.refresh_from_db()
        first_published_at = article.published_at
        self.assertIsNotNone(first_published_at)

        # بایگانی و انتشار مجدد تاریخ انتشار اولیه را حفظ می‌کند
        articles_services.ArchiveArticleService(article.id)
        article.status = 'PENDING'
        article.save(update_fields=['status'])
        republished = articles_services.PublishArticleService(article.id)
        self.assertEqual(republished.published_at, first_published_at)

    def test_reject_requires_reason(self):
        article = self._create_article()
        with self.assertRaises(ValueError):
            articles_services.RejectArticleService(article.id, '   ')

    def test_reject_stores_reason(self):
        article = self._create_article()
        rejected = articles_services.RejectArticleService(article.id, 'محتوای نامناسب')
        self.assertEqual(rejected.status, 'REJECTED')
        self.assertEqual(rejected.rejection_reason, 'محتوای نامناسب')

    def test_archive_only_from_published(self):
        article = self._create_article()
        with self.assertRaises(ValueError):
            articles_services.ArchiveArticleService(article.id)

        articles_services.PublishArticleService(article.id)
        archived = articles_services.ArchiveArticleService(article.id)
        self.assertEqual(archived.status, 'ARCHIVED')

    def test_toggle_featured_flips_flag(self):
        article = self._create_article()
        self.assertFalse(article.is_featured)

        articles_services.ToggleArticleFeaturedService(article.id)
        article.refresh_from_db()
        self.assertTrue(article.is_featured)

        articles_services.ToggleArticleFeaturedService(article.id)
        article.refresh_from_db()
        self.assertFalse(article.is_featured)


class DeleteArticleServiceTests(BaseArticleTestCase):
    """تست‌های حذف: مالکیت و پاک شدن گالری"""

    def test_owner_can_delete(self):
        article = self._create_article()
        articles_services.DeleteArticleService(article.id, requester=self.barber_user)
        self.assertFalse(
            articles_models.ArticleModel.objects.filter(id=article.id).exists()
        )

    def test_manager_can_delete_any(self):
        article = self._create_article()
        articles_services.DeleteArticleService(article.id, requester=self.manager)
        self.assertFalse(
            articles_models.ArticleModel.objects.filter(id=article.id).exists()
        )

    def test_non_owner_delete_fails(self):
        article = self._create_article()
        other = UserModel.objects.create_user(
            username='09122222222', phone_number='09122222222', role='CUSTOMER'
        )
        with self.assertRaises(ValueError):
            articles_services.DeleteArticleService(article.id, requester=other)


class ViewsCountServiceTests(BaseArticleTestCase):
    """تست شمارنده بازدید (افزایش اتمیک با F)"""

    def test_views_increment(self):
        article = self._create_article()
        articles_services.IncrementArticleViewsService(article.id)
        articles_services.IncrementArticleViewsService(article.id)
        article.refresh_from_db()
        self.assertEqual(article.views_count, 2)


class PublicQueryServiceTests(BaseArticleTestCase):
    """تست‌های کوئری‌های عمومی: انتشار، جستجو، فیلتر برچسب و مرتب‌سازی"""

    def test_published_list_excludes_pending(self):
        article = self._create_article()
        result = articles_services.GetPublishedArticlesService()
        self.assertEqual(len(result), 0)

        articles_services.PublishArticleService(article.id)
        result = articles_services.GetPublishedArticlesService()
        self.assertEqual(len(result), 1)

    def test_search_matches_title_and_content(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)

        by_title = articles_services.GetPublishedArticlesService(search='ریش')
        self.assertEqual(len(by_title), 1)

        by_content = articles_services.GetPublishedArticlesService(search='پاراگراف')
        self.assertEqual(len(by_content), 1)

        empty = articles_services.GetPublishedArticlesService(search='موجودی-وجود-ندارد')
        self.assertEqual(len(empty), 0)

    def test_filter_by_tag_slug(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)

        result = articles_services.GetPublishedArticlesService(tag_slug='اصلاح-مو')
        self.assertEqual(len(result), 1)

        other = articles_services.GetPublishedArticlesService(tag_slug='رنگ-مو')
        self.assertEqual(len(other), 0)

    def test_sort_by_views(self):
        first = self._create_article(title='مقاله کم‌بازدید')
        second = self._create_article(title='مقاله پرِبازدید')
        articles_services.PublishArticleService(first.id)
        articles_services.PublishArticleService(second.id)

        articles_services.IncrementArticleViewsService(second.id)
        articles_services.IncrementArticleViewsService(second.id)

        newest = articles_services.GetPublishedArticlesService(sort='newest')
        self.assertEqual(newest.first().id, second.id)

        by_views = articles_services.GetPublishedArticlesService(sort='views')
        self.assertEqual(by_views.first().id, second.id)
        self.assertEqual(by_views[1].id, first.id)

    def test_featured_returns_published_only(self):
        article = self._create_article(publish=True, author=self.manager, is_featured=True)
        result = articles_services.GetFeaturedArticlesService()
        self.assertEqual(len(result), 1)

    def test_get_by_slug_published_only(self):
        article = self._create_article()
        with self.assertRaises(ValueError):
            articles_services.GetArticleBySlugService(article.slug)

        articles_services.PublishArticleService(article.id)
        found = articles_services.GetArticleBySlugService(article.slug)
        self.assertEqual(found.id, article.id)

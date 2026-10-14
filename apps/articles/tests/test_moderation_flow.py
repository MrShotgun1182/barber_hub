from django.contrib.auth import get_user_model
from django.test import TestCase

from articles import models as articles_models
from articles import services as articles_services
from barbers import models as barbers_models
from tags import services as tags_services

from .test_article_services import BaseArticleTestCase, _make_image

UserModel = get_user_model()


class ModerationFlowTests(BaseArticleTestCase):
    """تست انتها-به-انتهای چرخه حیات مقاله: ساخت → انتشار → ویرایش → رد → حذف"""

    def test_full_lifecycle(self):
        # ۱. آرایشگر مقاله می‌نویسد و به صف بازبینی می‌رود
        article = self._create_article()
        self.assertEqual(article.status, 'PENDING')

        # ۲. مدیر انتشار می‌کند
        published = articles_services.PublishArticleService(article.id)
        self.assertEqual(published.status, 'PUBLISHED')

        # ۳. آرایشگر ویرایش می‌کند و مقاله دوباره در صف بازبینی قرار می‌گیرد
        # (تاریخ انتشار اولیه برای انتشار مجدد حفظ می‌شود)
        article.refresh_from_db()
        first_published_at = article.published_at

        edited = articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title=article.title,
            content='نسخه اصلاح‌شده محتوا',
        )
        self.assertEqual(edited.status, 'PENDING')
        self.assertEqual(edited.published_at, first_published_at)

        # ۴. مدیر با دلیل رد می‌کند؛ دلیل برای نویسنده ثبت می‌شود
        rejected = articles_services.RejectArticleService(article.id, 'نیازمند بازبینی منابع')
        self.assertEqual(rejected.status, 'REJECTED')
        self.assertEqual(rejected.rejection_reason, 'نیازمند بازبینی منابع')

        # ۵. نویسنده مقاله را حذف می‌کند
        articles_services.DeleteArticleService(article.id, requester=self.barber_user)
        self.assertFalse(
            articles_models.ArticleModel.objects.filter(id=article.id).exists()
        )

    def test_rejected_article_can_be_fixed_and_republished(self):
        # چرخه اصلاح: رد → ویرایش آرایشگر → انتشار مجدد
        article = self._create_article()
        articles_services.RejectArticleService(article.id, 'محتوای کوتاه')

        articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title=article.title,
            content='محتوای کامل و اصلاح‌شده',
        )
        republished = articles_services.PublishArticleService(article.id)
        self.assertEqual(republished.status, 'PUBLISHED')
        self.assertIsNone(republished.rejection_reason)

    def test_published_article_can_be_archived(self):
        article = self._create_article()
        articles_services.PublishArticleService(article.id)

        archived = articles_services.ArchiveArticleService(article.id)
        self.assertEqual(archived.status, 'ARCHIVED')

        # مقاله بایگانی‌شده در لیست عمومی نمایش داده نمی‌شود
        result = articles_services.GetPublishedArticlesService()
        self.assertEqual(len(result), 0)

    def test_manager_writes_and_publishes_directly(self):
        article = articles_services.CreateArticleService(
            author=self.manager,
            title='مقاله آموزشی مدیر',
            content='محتوای مقاله مدیر',
            cover_image=_make_image(),
            publish=True,
        )
        self.assertEqual(article.status, 'PUBLISHED')
        self.assertIsNotNone(article.published_at)

        # مقاله منتشرشده مدیر بلافاصله در لیست عمومی است
        result = articles_services.GetPublishedArticlesService()
        self.assertEqual(len(result), 1)


class TagAttachmentFlowTests(TestCase):
    """تست اتصال برچسب‌ها به مقاله در طول چرخه ویرایش"""

    def setUp(self):
        self.barber_user = UserModel.objects.create_user(
            username='09120000000',
            phone_number='09120000000',
            role='BARBER',
        )
        self.tag_a = tags_services.CreateTagService('اصلاح مو')
        self.tag_b = tags_services.CreateTagService('رنگ مو')

    def test_tags_replaced_on_update(self):
        article = articles_services.CreateArticleService(
            author=self.barber_user,
            title='مقاله با برچسب',
            content='محتوا',
            cover_image=_make_image(),
            tag_ids=[self.tag_a.id],
        )
        self.assertEqual(article.tags.count(), 1)

        articles_services.UpdateArticleService(
            article_id=article.id,
            editor=self.barber_user,
            title=article.title,
            content=article.content,
            tag_ids=[self.tag_a.id, self.tag_b.id],
        )
        self.assertEqual(article.tags.count(), 2)

        # حذف برچسب، فقط رابطه را قطع می‌کند نه خود مقاله را
        tags_services.DeleteTagService(self.tag_a.id)
        article.refresh_from_db()
        self.assertEqual(article.tags.count(), 1)
        self.assertEqual(article.tags.first().id, self.tag_b.id)

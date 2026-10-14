from django.db import transaction
from django.utils import timezone
from articles import models as articles_models


def PublishArticleService(article_id: int) -> articles_models.ArticleModel:
    """انتشار مقاله در انتظار تایید؛ تاریخ انتشار فقط بار اول ثبت می‌شود"""
    with transaction.atomic():
        try:
            article = articles_models.ArticleModel.objects.get(id=article_id)
        except articles_models.ArticleModel.DoesNotExist:
            raise ValueError('مقاله مورد نظر یافت نشد.')

        if article.status != 'PENDING':
            raise ValueError('فقط مقالات در انتظار تایید قابل انتشار هستند.')

        article.status = 'PUBLISHED'
        article.published_at = article.published_at or timezone.now()
        article.rejection_reason = None
        article.save(update_fields=['status', 'published_at', 'rejection_reason', 'updated_at'])
        return article


def RejectArticleService(article_id: int, reason: str) -> articles_models.ArticleModel:
    """رد مقاله در انتظار تایید همراه با دلیل برای نویسنده"""
    with transaction.atomic():
        try:
            article = articles_models.ArticleModel.objects.get(id=article_id)
        except articles_models.ArticleModel.DoesNotExist:
            raise ValueError('مقاله مورد نظر یافت نشد.')

        if article.status != 'PENDING':
            raise ValueError('فقط مقالات در انتظار تایید قابل رد کردن هستند.')

        if not reason or not reason.strip():
            raise ValueError('دلیل رد مقاله الزامی است.')

        article.status = 'REJECTED'
        article.rejection_reason = reason.strip()
        article.save(update_fields=['status', 'rejection_reason', 'updated_at'])
        return article


def ArchiveArticleService(article_id: int) -> articles_models.ArticleModel:
    """بایگانی مقاله منتشرشده (مخفی از عموم بدون حذف)"""
    with transaction.atomic():
        try:
            article = articles_models.ArticleModel.objects.get(id=article_id)
        except articles_models.ArticleModel.DoesNotExist:
            raise ValueError('مقاله مورد نظر یافت نشد.')

        if article.status != 'PUBLISHED':
            raise ValueError('فقط مقالات منتشرشده قابل بایگانی هستند.')

        article.status = 'ARCHIVED'
        article.save(update_fields=['status', 'updated_at'])
        return article


def ToggleArticleFeaturedService(article_id: int) -> articles_models.ArticleModel:
    """تغییر وضعیت ویژه بودن مقاله (فقط مدیر)"""
    with transaction.atomic():
        try:
            article = articles_models.ArticleModel.objects.get(id=article_id)
        except articles_models.ArticleModel.DoesNotExist:
            raise ValueError('مقاله مورد نظر یافت نشد.')

        article.is_featured = not article.is_featured
        article.save(update_fields=['is_featured', 'updated_at'])
        return article

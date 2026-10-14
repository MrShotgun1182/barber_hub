from django.db import transaction
from django.utils import timezone
from articles import models as articles_models
from articles.services.generate_article_slug_service import GenerateArticleSlugService
from tags import models as tags_models


def UpdateArticleService(
    article_id: int,
    editor,
    title: str,
    content: str,
    cover_image=None,
    tag_ids: list = None,
    gallery_files: list = None,
    publish: bool = False,
) -> articles_models.ArticleModel:
    """به‌روزرسانی مقاله؛ ذخیره مجدد توسط آرایشگر مقاله را به صف بازبینی برمی‌گرداند"""
    with transaction.atomic():
        # ۱. دریافت مقاله و بررسی مالکیت
        try:
            article = articles_models.ArticleModel.objects.get(id=article_id)
        except articles_models.ArticleModel.DoesNotExist:
            raise ValueError('مقاله مورد نظر یافت نشد.')

        is_manager = getattr(editor, 'role', None) == 'MANAGER' or editor.is_staff or editor.is_superuser
        if article.author_id != editor.id and not is_manager:
            raise ValueError('اجازه ویرایش این مقاله را ندارید.')

        # ۲. اعتبارسنجی فیلدهای الزامی
        if not title or not title.strip():
            raise ValueError('عنوان مقاله الزامی است.')

        if not content or not content.strip():
            raise ValueError('محتوای مقاله الزامی است.')

        # ۳. اعتبارسنجی برچسب‌های انتخاب‌شده
        valid_tags = None
        if tag_ids is not None:
            valid_tags = list(tags_models.TagModel.objects.filter(id__in=tag_ids))
            if len(valid_tags) != len(set(tag_ids)):
                raise ValueError('یکی از برچسب‌های انتخاب‌شده یافت نشد.')

        # ۴. به‌روزرسانی فیلدها؛ اسلاگ فقط با تغییر عنوان بازتولید می‌شود
        new_title = title.strip()
        if article.title != new_title:
            article.slug = GenerateArticleSlugService(new_title, exclude_id=article.id)
        article.title = new_title
        article.content = content
        if cover_image is not None:
            article.cover_image = cover_image

        if valid_tags is not None:
            article.tags.set(valid_tags)

        # ۵. افزودن تصاویر گالری جدید در ادامه تصاویر موجود
        start_index = article.images.count()
        for index, image_file in enumerate(gallery_files or []):
            articles_models.ArticleImageModel.objects.create(
                article=article,
                image=image_file,
                sort_order=start_index + index,
            )

        # ۶. تعیین وضعیت: انتشار مستقیم فقط برای مدیر؛ در غیر این صورت بازبینی مجدد
        if publish:
            if not is_manager:
                raise ValueError('فقط مدیر می‌تواند مقاله را مستقیماً منتشر کند.')
            article.status = 'PUBLISHED'
            article.published_at = article.published_at or timezone.now()
            article.rejection_reason = None
        else:
            article.status = 'PENDING'
            article.rejection_reason = None

        article.save()
        return article

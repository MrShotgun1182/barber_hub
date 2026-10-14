from django.db import transaction
from django.utils import timezone
from articles import models as articles_models
from articles.services.generate_article_slug_service import GenerateArticleSlugService
from tags import models as tags_models


def CreateArticleService(
    author,
    title: str,
    content: str,
    cover_image,
    tag_ids: list = None,
    gallery_files: list = None,
    publish: bool = False,
    is_featured: bool = False,
) -> articles_models.ArticleModel:
    """ساخت مقاله جدید همراه با برچسب‌ها و تصاویر گالری (اتمیک)"""
    with transaction.atomic():
        # ۱. اعتبارسنجی فیلدهای الزامی
        if not title or not title.strip():
            raise ValueError('عنوان مقاله الزامی است.')

        if not content or not content.strip():
            raise ValueError('محتوای مقاله الزامی است.')

        if cover_image is None:
            raise ValueError('تصویر شاخص الزامی است.')

        # ۲. اعتبارسنجی برچسب‌های انتخاب‌شده
        valid_tags = []
        if tag_ids:
            valid_tags = list(tags_models.TagModel.objects.filter(id__in=tag_ids))
            if len(valid_tags) != len(set(tag_ids)):
                raise ValueError('یکی از برچسب‌های انتخاب‌شده یافت نشد.')

        # ۳. انتشار مستقیم فقط برای مدیر؛ در غیر این صورت مقاله به صف بازبینی می‌رود
        if publish and getattr(author, 'role', None) != 'MANAGER' and not (
            author.is_staff or author.is_superuser
        ):
            raise ValueError('فقط مدیر می‌تواند مقاله را مستقیماً منتشر کند.')

        # ۴. ساخت مقاله با اسلاگ خودکار
        article = articles_models.ArticleModel.objects.create(
            title=title.strip(),
            slug=GenerateArticleSlugService(title),
            author=author,
            cover_image=cover_image,
            content=content,
            is_featured=is_featured,
            status='PUBLISHED' if publish else 'PENDING',
            published_at=timezone.now() if publish else None,
        )

        # ۵. ثبت برچسب‌ها و تصاویر گالری
        if valid_tags:
            article.tags.set(valid_tags)

        for index, image_file in enumerate(gallery_files or []):
            articles_models.ArticleImageModel.objects.create(
                article=article,
                image=image_file,
                sort_order=index,
            )

        return article

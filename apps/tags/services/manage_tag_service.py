from django.db import transaction
from django.utils.text import slugify
from tags import models as tags_models


def GenerateTagSlugService(name: str, exclude_id: int = None) -> str:
    """تولید اسلاگ فارسی یکتا از نام برچسب"""
    base = slugify(name, allow_unicode=True) or 'tag'

    # ۱. اگر خود نام یکتا باشد، همان اسلاگ پایه برگردد
    queryset = tags_models.TagModel.objects.exclude(id=exclude_id)
    if not queryset.filter(slug=base).exists():
        return base

    # ۲. در صورت تداخل، پسوند عددی افزایشی تا یکتا شدن
    counter = 2
    while queryset.filter(slug=f'{base}-{counter}').exists():
        counter += 1
    return f'{base}-{counter}'


def CreateTagService(name: str) -> tags_models.TagModel:
    """ساخت برچسب جدید با اسلاگ خودکار"""
    with transaction.atomic():
        if not name or not name.strip():
            raise ValueError('نام برچسب الزامی است.')

        name = name.strip()

        if tags_models.TagModel.objects.filter(name=name).exists():
            raise ValueError('برچسبی با این نام از قبل وجود دارد.')

        return tags_models.TagModel.objects.create(
            name=name,
            slug=GenerateTagSlugService(name),
        )


def UpdateTagService(tag_id: int, name: str) -> tags_models.TagModel:
    """به‌روزرسانی نام برچسب و بازتولید اسلاگ در صورت تغییر نام"""
    with transaction.atomic():
        if not name or not name.strip():
            raise ValueError('نام برچسب الزامی است.')

        name = name.strip()

        try:
            tag = tags_models.TagModel.objects.get(id=tag_id)
        except tags_models.TagModel.DoesNotExist:
            raise ValueError('برچسب مورد نظر یافت نشد.')

        if tag.name != name:
            if tags_models.TagModel.objects.filter(name=name).exclude(id=tag.id).exists():
                raise ValueError('برچسبی با این نام از قبل وجود دارد.')
            tag.name = name
            tag.slug = GenerateTagSlugService(name, exclude_id=tag.id)
            tag.save(update_fields=['name', 'slug'])

        return tag


def DeleteTagService(tag_id: int) -> None:
    """حذف برچسب (فقط رابطه با مقالات را قطع می‌کند)"""
    with transaction.atomic():
        try:
            tag = tags_models.TagModel.objects.get(id=tag_id)
        except tags_models.TagModel.DoesNotExist:
            raise ValueError('برچسب مورد نظر یافت نشد.')

        tag.delete()

from django.utils.text import slugify
from articles import models as articles_models


def GenerateArticleSlugService(title: str, exclude_id: int = None) -> str:
    """تولید اسلاگ فارسی یکتا از عنوان مقاله"""
    base = slugify(title, allow_unicode=True) or 'article'

    # ۱. اگر خود عنوان یکتا باشد، همان اسلاگ پایه برگردد
    queryset = articles_models.ArticleModel.objects.exclude(id=exclude_id)
    if not queryset.filter(slug=base).exists():
        return base

    # ۲. در صورت تداخل، پسوند عددی افزایشی تا یکتا شدن
    counter = 2
    while queryset.filter(slug=f'{base}-{counter}').exists():
        counter += 1
    return f'{base}-{counter}'

from django.db.models import Q
from articles import models as articles_models


def GetPublishedArticlesService(
    search: str = None,
    tag_slug: str = None,
    author_id: int = None,
    sort: str = 'newest',
):
    """دریافت مقالات منتشرشده با جستجو، فیلتر برچسب/نویسنده و مرتب‌سازی"""
    queryset = articles_models.ArticleModel.objects.filter(
        status='PUBLISHED'
    ).select_related('author').prefetch_related('tags', 'images')

    # ۱. جستجوی کلیدواژه در عنوان و متن مقاله
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )

    # ۲. فیلتر برچسب (distinct به‌خاطر join جدول M2M)
    if tag_slug:
        queryset = queryset.filter(tags__slug=tag_slug).distinct()

    # ۳. فیلتر نویسنده
    if author_id:
        queryset = queryset.filter(author_id=author_id)

    # ۴. مرتب‌سازی: جدیدترین یا پربازدیدترین
    if sort == 'views':
        queryset = queryset.order_by('-views_count', '-published_at')
    else:
        queryset = queryset.order_by('-published_at', '-created_at')

    return queryset


def GetFeaturedArticlesService():
    """دریافت مقالات ویژه منتشرشده برای بخش ویژه صفحه عمومی"""
    return (
        articles_models.ArticleModel.objects.filter(
            status='PUBLISHED', is_featured=True
        )
        .select_related('author')
        .prefetch_related('tags')[:4]
    )

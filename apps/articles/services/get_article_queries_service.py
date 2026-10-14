from articles import models as articles_models


def GetArticleBySlugService(slug: str) -> articles_models.ArticleModel:
    """دریافت مقاله منتشرشده بر اساس اسلاگ"""
    try:
        return articles_models.ArticleModel.objects.select_related('author').prefetch_related(
            'tags', 'images'
        ).get(slug=slug, status='PUBLISHED')
    except articles_models.ArticleModel.DoesNotExist:
        raise ValueError('مقاله مورد نظر یافت نشد.')


def GetArticleByIdService(article_id: int) -> articles_models.ArticleModel:
    """دریافت مقاله بر اساس شناسه (برای فرم ویرایش)"""
    try:
        return articles_models.ArticleModel.objects.select_related('author').prefetch_related(
            'tags', 'images'
        ).get(id=article_id)
    except articles_models.ArticleModel.DoesNotExist:
        raise ValueError('مقاله مورد نظر یافت نشد.')


def GetArticlesByAuthorService(author):
    """دریافت همه مقالات یک نویسنده (برای لیست پنل آرایشگر)"""
    return articles_models.ArticleModel.objects.filter(
        author=author
    ).prefetch_related('tags')


def GetArticlesForModerationService(status: str = None, search: str = None):
    """دریافت همه مقالات برای صف بازبینی مدیر با فیلتر وضعیت و جستجو"""
    queryset = articles_models.ArticleModel.objects.select_related('author').prefetch_related(
        'tags'
    )

    # ۱. فیلتر وضعیت (فقط وضعیت‌های معتبر جریان بازبینی)
    if status in ('PENDING', 'PUBLISHED', 'REJECTED', 'ARCHIVED'):
        queryset = queryset.filter(status=status)

    # ۲. جستجو در عنوان
    if search:
        queryset = queryset.filter(title__icontains=search)

    return queryset.order_by('-updated_at')


def GetPublishedAuthorsService():
    """دریافت نویسندگان مقالات منتشرشده برای فیلتر صفحه عمومی"""
    return list(
        articles_models.ArticleModel.objects.filter(status='PUBLISHED')
        .values('author_id', 'author__username')
        .distinct()
        .order_by('author__username')
    )

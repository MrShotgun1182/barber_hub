from store import models as store_models


def GetPublishedProductsService(category_id: int = None, search: str = None):
    """دریافت محصولات منتشرشده و حذف‌نشده (به تفکیک دسته‌بندی در صورت ارسال)"""
    queryset = store_models.ProductModel.objects.filter(
        is_published=True, is_deleted=False
    ).prefetch_related('images')

    if category_id is not None:
        queryset = queryset.filter(category_id=category_id)

    if search:
        queryset = queryset.filter(title__icontains=search)

    return queryset

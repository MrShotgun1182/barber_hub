from store import models as store_models


def GetAllProductsService():
    """دریافت همه محصولات (شامل منتشرنشده) برای پنل مدیر"""
    return store_models.ProductModel.objects.filter(
        is_deleted=False
    ).select_related('category').prefetch_related('images')

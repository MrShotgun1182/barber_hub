from store import models as store_models


def GetProductDetailService(product_id: int) -> store_models.ProductModel:
    """دریافت یک محصول منتشرشده همراه با تصاویر برای صفحه جزئیات"""
    try:
        return store_models.ProductModel.objects.prefetch_related('images').get(
            id=product_id, is_published=True, is_deleted=False
        )
    except store_models.ProductModel.DoesNotExist:
        raise ValueError('محصول مورد نظر یافت نشد.')

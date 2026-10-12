from store import models as store_models


def DeleteProductService(product_id: int) -> None:
    """حذف نرم محصول (سابقه سفارش‌ها دست‌نخورده می‌ماند)"""
    try:
        product = store_models.ProductModel.objects.get(id=product_id, is_deleted=False)
    except store_models.ProductModel.DoesNotExist:
        raise ValueError('محصول مورد نظر یافت نشد.')

    product.is_deleted = True
    product.is_published = False
    product.is_orderable = False
    product.save(update_fields=['is_deleted', 'is_published', 'is_orderable'])

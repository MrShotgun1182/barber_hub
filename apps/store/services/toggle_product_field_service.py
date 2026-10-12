from store import models as store_models


def ToggleProductFieldService(product_id: int, field: str) -> store_models.ProductModel:
    """تغییر سریع وضعیت انتشار یا قابل‌سفارش بودن محصول"""
    if field not in ('is_published', 'is_orderable'):
        raise ValueError('فیلد قابل تغییر نیست.')

    try:
        product = store_models.ProductModel.objects.get(id=product_id, is_deleted=False)
    except store_models.ProductModel.DoesNotExist:
        raise ValueError('محصول مورد نظر یافت نشد.')

    setattr(product, field, not getattr(product, field))
    product.save(update_fields=[field, 'updated_at'])
    return product

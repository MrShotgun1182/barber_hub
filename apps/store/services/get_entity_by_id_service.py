from store import models as store_models


def GetCategoryByIdService(category_id: int):
    """دریافت دسته‌بندی بر اساس شناسه؛ اگر نبود None برمی‌گردد"""
    try:
        return store_models.CategoryModel.objects.get(pk=category_id)
    except store_models.CategoryModel.DoesNotExist:
        return None


def GetProductByIdService(product_id: int):
    """دریافت محصول بر اساس شناسه؛ اگر نبود None برمی‌گردد"""
    try:
        return store_models.ProductModel.objects.prefetch_related('images').get(
            pk=product_id
        )
    except store_models.ProductModel.DoesNotExist:
        return None


def GetOrderByIdService(order_id: int):
    """دریافت سفارش بر اساس شناسه؛ اگر نبود None برمی‌گردد"""
    try:
        return (
            store_models.OrderModel.objects.select_related('customer', 'customer__user')
            .prefetch_related('items', 'payments')
            .get(pk=order_id)
        )
    except store_models.OrderModel.DoesNotExist:
        return None

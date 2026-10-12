from django.db import models
from store import models as store_models


def DeleteCategoryService(category_id: int) -> None:
    """حذف دسته‌بندی (فقط در صورت نداشتن محصول)"""
    try:
        category = store_models.CategoryModel.objects.get(id=category_id)
    except store_models.CategoryModel.DoesNotExist:
        raise ValueError('دسته‌بندی مورد نظر یافت نشد.')

    if store_models.ProductModel.objects.filter(category=category).exists():
        raise ValueError('این دسته‌بندی دارای محصول است و قابل حذف نیست.')

    category.delete()

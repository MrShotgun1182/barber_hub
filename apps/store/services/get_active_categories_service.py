from store import models as store_models


def GetActiveCategoriesService():
    """دریافت دسته‌بندی‌های فعال برای نمایش به مشتری"""
    return store_models.CategoryModel.objects.filter(is_active=True)

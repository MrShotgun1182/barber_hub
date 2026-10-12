from store import models as store_models


def GetAllCategoriesService():
    """دریافت همه دسته‌بندی‌ها برای پنل مدیر"""
    return store_models.CategoryModel.objects.all()

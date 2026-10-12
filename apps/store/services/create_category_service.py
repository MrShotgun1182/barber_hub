from django.db import transaction
from store import models as store_models


def CreateCategoryService(name: str, description: str = None, is_active: bool = True) -> store_models.CategoryModel:
    """ساخت دسته‌بندی محصول جدید"""
    if not name or not name.strip():
        raise ValueError('نام دسته‌بندی الزامی است.')

    if store_models.CategoryModel.objects.filter(name=name.strip()).exists():
        raise ValueError('دسته‌بندی با این نام قبلاً ثبت شده است.')

    return store_models.CategoryModel.objects.create(
        name=name.strip(),
        description=description,
        is_active=is_active,
    )

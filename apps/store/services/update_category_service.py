from store import models as store_models


def UpdateCategoryService(category_id: int, **fields) -> store_models.CategoryModel:
    """ویرایش دسته‌بندی محصول"""
    try:
        category = store_models.CategoryModel.objects.get(id=category_id)
    except store_models.CategoryModel.DoesNotExist:
        raise ValueError('دسته‌بندی مورد نظر یافت نشد.')

    allowed_fields = {'name', 'description', 'is_active'}
    for field, value in fields.items():
        if field not in allowed_fields:
            continue
        if field == 'name':
            value = (value or '').strip()
            if not value:
                raise ValueError('نام دسته‌بندی الزامی است.')
            if store_models.CategoryModel.objects.exclude(id=category_id).filter(name=value).exists():
                raise ValueError('دسته‌بندی با این نام قبلاً ثبت شده است.')
        setattr(category, field, value)

    category.save()
    return category

from django.db import transaction
from store import models as store_models


def UpdateProductService(product_id: int, image_files: list = None, **fields) -> store_models.ProductModel:
    """ویرایش محصول و افزودن تصاویر جدید (اتمیک)"""
    with transaction.atomic():
        try:
            product = store_models.ProductModel.objects.get(id=product_id, is_deleted=False)
        except store_models.ProductModel.DoesNotExist:
            raise ValueError('محصول مورد نظر یافت نشد.')

        allowed_fields = {'title', 'description', 'price', 'category', 'is_published', 'is_orderable'}
        for field, value in fields.items():
            if field == 'title':
                value = (value or '').strip()
                if not value:
                    raise ValueError('عنوان محصول الزامی است.')
            if field == 'price' and (value is None or value < 0):
                raise ValueError('قیمت محصول نامعتبر است.')
            if field == 'category' and value is not None:
                if not store_models.CategoryModel.objects.filter(id=value).exists():
                    raise ValueError('دسته‌بندی مورد نظر یافت نشد.')
            if field in allowed_fields:
                setattr(product, field, value)

        product.save()

        # ۱. افزودن تصاویر جدید پس از آخرین تصویر موجود
        if image_files:
            last_order = product.images.count()
            for index, image_file in enumerate(image_files):
                store_models.ProductImageModel.objects.create(
                    product=product,
                    image=image_file,
                    is_main=False,
                    sort_order=last_order + index,
                )

        return product

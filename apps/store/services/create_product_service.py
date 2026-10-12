from django.db import transaction
from store import models as store_models


def CreateProductService(
    title: str,
    price: int,
    category_id: int,
    description: str = None,
    is_published: bool = False,
    is_orderable: bool = True,
    image_files: list = None,
) -> store_models.ProductModel:
    """ساخت محصول جدید همراه با تصاویر (اتمیک)"""
    with transaction.atomic():
        if not title or not title.strip():
            raise ValueError('عنوان محصول الزامی است.')

        if price is None or price < 0:
            raise ValueError('قیمت محصول نامعتبر است.')

        try:
            category = store_models.CategoryModel.objects.get(id=category_id)
        except store_models.CategoryModel.DoesNotExist:
            raise ValueError('دسته‌بندی مورد نظر یافت نشد.')

        product = store_models.ProductModel.objects.create(
            title=title.strip(),
            description=description,
            price=price,
            category=category,
            is_published=is_published,
            is_orderable=is_orderable,
        )

        # ۱. ذخیره تصاویر ارسالی (اولین تصویر به‌عنوان تصویر اصلی)
        for index, image_file in enumerate(image_files or []):
            store_models.ProductImageModel.objects.create(
                product=product,
                image=image_file,
                is_main=(index == 0),
                sort_order=index,
            )

        return product

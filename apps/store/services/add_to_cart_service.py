from django.db import transaction
from store import models as store_models
from store.services.get_or_create_cart_service import GetOrCreateCartService


def AddToCartService(customer, product_id: int, quantity: int = 1) -> store_models.CartItemModel:
    """افزودن محصول به سبد خرید یا افزایش تعداد آن به‌صورت اتمیک"""
    with transaction.atomic():
        # ۱. اعتبارسنجی وجود و قابل سفارش بودن محصول
        try:
            product = store_models.ProductModel.objects.get(
                id=product_id, is_published=True, is_deleted=False
            )
        except store_models.ProductModel.DoesNotExist:
            raise ValueError('محصول مورد نظر یافت نشد.')

        if not product.is_orderable:
            raise ValueError('این محصول در حال حاضر قابل سفارش نیست.')

        if quantity < 1:
            raise ValueError('تعداد باید حداقل ۱ باشد.')

        # ۲. دریافت سبد و افزودن/افزایش آیتم (قیمت مرجع فقط هنگام ایجاد ثبت می‌شود)
        cart = GetOrCreateCartService(customer)
        item, created = store_models.CartItemModel.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'unit_price': product.price},
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=['quantity'])

        return item

from django.db import models
from store import models as store_models


class CartItemModel(models.Model):
    cart = models.ForeignKey(
        store_models.CartModel,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سبد خرید',
    )
    product = models.ForeignKey(
        store_models.ProductModel,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='محصول',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    # قیمت لحظه افزودن به سبد — صرفاً مرجع تشخیص تغییر قیمت؛ جمع کل همیشه از قیمت زنده محاسبه می‌شود
    unit_price = models.PositiveIntegerField(
        default=0, verbose_name='قیمت هنگام افزودن'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن')

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'
        ordering = ['added_at']

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"

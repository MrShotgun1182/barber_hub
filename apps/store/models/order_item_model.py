from django.db import models
from store import models as store_models


class OrderItemModel(models.Model):
    order = models.ForeignKey(
        store_models.OrderModel,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش',
    )
    product = models.ForeignKey(
        store_models.ProductModel,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='محصول',
    )
    product_title = models.CharField(
        max_length=200, verbose_name='عنوان محصول در زمان سفارش'
    )
    unit_price = models.PositiveIntegerField(
        verbose_name='قیمت واحد در زمان سفارش (تومان)'
    )
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    line_total = models.PositiveIntegerField(verbose_name='جمع ردیف (تومان)')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
        ordering = ['id']

    def __str__(self):
        return f"{self.product_title} × {self.quantity}"

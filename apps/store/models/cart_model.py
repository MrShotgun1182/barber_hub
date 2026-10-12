from django.db import models
from customers import models as customers_models


class CartModel(models.Model):
    customer = models.OneToOneField(
        customers_models.CustomerModel,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='مشتری',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def __str__(self):
        return f"سبد خرید {self.customer.user.username}"

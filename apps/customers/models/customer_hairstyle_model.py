from django.db import models
from customers import models as customers_models


class CustomerHairstyleModel(models.Model):
    customer = models.ForeignKey(
        customers_models.CustomerModel,
        on_delete=models.CASCADE,
        related_name='hairstyles',
        verbose_name='مشتری',
    )
    image = models.ImageField(
        upload_to='customers/hairstyles/',
        verbose_name='تصویر مدل مو',
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='عنوان / نام مدل مو',
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات و یادداشت آرایشگر',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت',
    )

    class Meta:
        verbose_name = 'مدل موی مشتری'
        verbose_name_plural = 'مدل‌های موی مشتریان'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.user.username} - {self.title or 'تصویر مدل مو'}"
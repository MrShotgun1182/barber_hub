from django.db import models
from customers import models as customers_models


class OrderModel(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING_PAYMENT', 'در انتظار پرداخت'),
        ('PLACED', 'ثبت‌شده'),
        ('VIEWED', 'بررسی‌شده'),
        ('READY_FOR_PICKUP', 'آماده تحویل'),
        ('DELIVERED', 'تحویل‌شده'),
        ('CANCELLED', 'لغوشده'),
    )

    order_number = models.CharField(
        max_length=20, unique=True, verbose_name='شماره سفارش'
    )
    customer = models.ForeignKey(
        customers_models.CustomerModel,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='مشتری',
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='PENDING_PAYMENT',
        verbose_name='وضعیت سفارش',
    )
    total_amount = models.PositiveIntegerField(verbose_name='مبلغ کل (تومان)')
    customer_full_name = models.CharField(
        max_length=150, blank=True, verbose_name='نام مشتری (در زمان سفارش)'
    )
    customer_phone = models.CharField(
        max_length=15, blank=True, verbose_name='شماره تماس (در زمان سفارش)'
    )
    customer_note = models.TextField(blank=True, null=True, verbose_name='توضیحات مشتری')
    idempotency_key = models.CharField(
        max_length=64, unique=True, null=True, blank=True,
        verbose_name='کلید یکتایی ثبت',
        help_text='برای جلوگیری از ثبت تکراری سفارش در درخواست‌های مکرر.',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.customer.user.username}"

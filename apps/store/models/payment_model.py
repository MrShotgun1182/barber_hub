from django.db import models
from store import models as store_models


class PaymentModel(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('INITIATED', 'آغازشده'),
        ('VERIFIED', 'تأییدشده'),
        ('FAILED', 'ناموفق'),
        ('CANCELLED', 'لغوشده'),
    )

    order = models.ForeignKey(
        store_models.OrderModel,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name='سفارش',
    )
    authority = models.CharField(
        max_length=100, unique=True, null=True, blank=True,
        verbose_name='شناسه تراکنش درگاه',
    )
    ref_id = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='شماره پیگیری پرداخت'
    )
    amount = models.PositiveIntegerField(verbose_name='مبلغ (تومان)')
    gateway = models.CharField(
        max_length=20, default='ZARINPAL', verbose_name='درگاه پرداخت'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='INITIATED',
        verbose_name='وضعیت پرداخت',
    )
    gateway_code = models.IntegerField(
        null=True, blank=True, verbose_name='کد پاسخ درگاه'
    )
    failure_message = models.CharField(
        max_length=255, blank=True, verbose_name='پیام خطای درگاه'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ تأیید')

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"پرداخت {self.order.order_number} - {self.get_status_display()}"

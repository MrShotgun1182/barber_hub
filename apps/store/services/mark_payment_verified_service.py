from django.utils import timezone
from store import models as store_models


def MarkPaymentVerifiedService(payment, ref_id: str, code: int) -> store_models.PaymentModel:
    """ثبت پرداخت به‌عنوان تأییدشده همراه با شماره پیگیری"""
    payment.ref_id = str(ref_id)
    payment.gateway_code = code
    payment.status = 'VERIFIED'
    payment.verified_at = timezone.now()
    payment.save(update_fields=['ref_id', 'gateway_code', 'status', 'verified_at'])
    return payment

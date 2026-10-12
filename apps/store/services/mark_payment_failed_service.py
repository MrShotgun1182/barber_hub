from store import models as store_models


def MarkPaymentFailedService(payment, code: int = None, message: str = '') -> store_models.PaymentModel:
    """ثبت پرداخت به‌عنوان ناموفق یا لغوشده"""
    payment.gateway_code = code
    payment.failure_message = message or ''
    payment.status = 'FAILED'
    payment.save(update_fields=['gateway_code', 'failure_message', 'status'])
    return payment

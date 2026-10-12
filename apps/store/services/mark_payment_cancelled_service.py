from store import models as store_models


def MarkPaymentCancelledService(payment) -> None:
    """لغو رکورد پرداخت (بازگشت ناموفق یا انصراف مشتری از درگاه)"""
    payment.status = 'CANCELLED'
    store_models.PaymentModel.objects.filter(pk=payment.pk).update(
        status='CANCELLED'
    )

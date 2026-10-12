from store import models as store_models


def GetPaymentByAuthorityService(authority: str) -> store_models.PaymentModel:
    """یافتن پرداخت با شناسه تراکنش درگاه به‌صورت قفل‌شده (اتمیک)"""
    try:
        return store_models.PaymentModel.objects.select_for_update().get(
            authority=authority
        )
    except store_models.PaymentModel.DoesNotExist:
        raise ValueError('تراکنش مورد نظر یافت نشد.')

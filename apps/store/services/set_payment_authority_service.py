from store import models as store_models


def SetPaymentAuthorityService(payment, authority: str) -> store_models.PaymentModel:
    """ذخیره شناسه تراکنش (authority) دریافتی از درگاه پرداخت"""
    payment.authority = authority
    payment.save(update_fields=['authority'])
    return payment

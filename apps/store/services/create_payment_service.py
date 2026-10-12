from store import models as store_models


def CreatePaymentService(order) -> store_models.PaymentModel:
    """ساخت رکورد پرداخت با وضعیت INITIATED برای یک سفارش"""
    return store_models.PaymentModel.objects.create(
        order=order,
        amount=order.total_amount,
        status='INITIATED',
    )

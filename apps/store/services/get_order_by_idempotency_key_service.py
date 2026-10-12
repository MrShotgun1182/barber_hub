from store import models as store_models


def GetOrderByIdempotencyKeyService(idempotency_key: str):
    """دریافت سفارش بر اساس کلید idempotency (بازپخش ثبت تکراری)؛ اگر نبود None برمی‌گردد"""
    try:
        return store_models.OrderModel.objects.get(idempotency_key=idempotency_key)
    except store_models.OrderModel.DoesNotExist:
        return None

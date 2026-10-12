from store import models as store_models


def GetCustomerOrderDetailService(customer, order_id: int) -> dict:
    """دریافت جزئیات یک سفارش صرفاً در صورت تعلق به همان مشتری"""
    try:
        order = (
            store_models.OrderModel.objects
            .select_related('customer', 'customer__user')
            .prefetch_related('items', 'payments')
            .get(id=order_id, customer=customer)
        )
    except store_models.OrderModel.DoesNotExist:
        raise ValueError('سفارش مورد نظر یافت نشد.')

    return {
        'order': order,
        'items': list(order.items.all()),
        'payments': list(order.payments.all()),
    }

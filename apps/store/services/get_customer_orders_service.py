from store import models as store_models


def GetCustomerOrdersService(customer) -> list:
    """دریافت تاریخچه سفارش‌های خودِ مشتری"""
    orders = store_models.OrderModel.objects.filter(
        customer=customer
    ).prefetch_related('items', 'payments')

    rows = []
    for order in orders:
        rows.append({
            'id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'total_amount': order.total_amount,
            'created_at': order.created_at,
            'is_paid': order.payments.filter(status='VERIFIED').exists(),
        })
    return rows

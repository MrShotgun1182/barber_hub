from store import models as store_models

# گذارهای مجاز وضعیت سفارش (لغو فقط توسط مدیر انجام می‌شود)
ALLOWED_TRANSITIONS = {
    'PENDING_PAYMENT': ['CANCELLED'],
    'PLACED': ['VIEWED', 'CANCELLED'],
    'VIEWED': ['READY_FOR_PICKUP', 'CANCELLED'],
    'READY_FOR_PICKUP': ['DELIVERED', 'CANCELLED'],
    'DELIVERED': [],
    'CANCELLED': [],
}


def UpdateOrderStatusService(order, new_status: str) -> store_models.OrderModel:
    """تغییر وضعیت سفارش با اعتبارسنجی گذار مجاز"""
    if new_status not in dict(store_models.OrderModel.ORDER_STATUS_CHOICES):
        raise ValueError('وضعیت نامعتبر است.')

    # «ثبت‌شده» تنها از «در انتظار پرداخت» و فقط پس از تأیید پرداخت ممکن است
    if new_status == 'PLACED' and order.status == 'PENDING_PAYMENT':
        if not order.payments.filter(status='VERIFIED').exists():
            raise ValueError(
                'سفارش بدون پرداخت تأییدشده نمی‌تواند به حالت «ثبت‌شده» برود.'
            )
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        return order

    allowed = ALLOWED_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        raise ValueError('تغییر وضعیت از حالت فعلی مجاز نیست.')

    order.status = new_status
    order.save(update_fields=['status', 'updated_at'])
    return order

from store import models as store_models


def GetAllOrdersService(status: str = None):
    """دریافت همه سفارش‌ها برای پنل مدیر (با فیلتر وضعیت در صورت ارسال)"""
    queryset = store_models.OrderModel.objects.select_related(
        'customer', 'customer__user'
    ).prefetch_related('items', 'payments')

    if status:
        queryset = queryset.filter(status=status)

    return queryset

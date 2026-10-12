from store import models as store_models
from store import services as store_services


def GetManageOrdersAction(status: str = None) -> dict:
    """اکشن دریافت لیست سفارش‌ها برای پنل مدیر"""
    try:
        orders = list(store_services.GetAllOrdersService(status=status))
        return {'status': 'success', 'message': '', 'orders': orders}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت سفارش‌ها.'}


def UpdateOrderStatusAction(order_id: int, new_status: str) -> dict:
    """اکشن تغییر وضعیت سفارش توسط مدیر (با اعتبارسنجی گذارهای مجاز)"""
    try:
        order = store_models.OrderModel.objects.get(pk=order_id)
        store_services.UpdateOrderStatusService(order, new_status)
        return {
            'status': 'success',
            'message': 'وضعیت سفارش با موفقیت تغییر کرد.',
            'order': order,
        }
    except store_models.OrderModel.DoesNotExist:
        return {'status': 'error', 'message': 'سفارش مورد نظر یافت نشد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در تغییر وضعیت سفارش.'}

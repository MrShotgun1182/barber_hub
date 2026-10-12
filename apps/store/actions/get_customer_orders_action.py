from customers import models as customers_models
from store import services as store_services


def GetCustomerOrdersAction(user) -> dict:
    """اکشن دریافت لیست سفارش‌های مشتری"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        orders = list(store_services.GetCustomerOrdersService(customer))
        return {'status': 'success', 'message': '', 'orders': orders}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت سفارش‌ها.'}

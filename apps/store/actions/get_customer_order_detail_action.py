from customers import models as customers_models
from store import services as store_services


def GetCustomerOrderDetailAction(user, order_id: int) -> dict:
    """اکشن دریافت جزئیات یک سفارش مشتری"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        result = store_services.GetCustomerOrderDetailService(customer, order_id)
        return {'status': 'success', 'message': '', **result}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت جزئیات سفارش.'}

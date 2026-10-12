from customers import models as customers_models
from store import services as store_services


def GetCartAction(user) -> dict:
    """اکشن دریافت جمع‌بندی سبد خرید مشتری"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        summary = store_services.GetCartSummaryService(customer)
        return {'status': 'success', 'message': '', **summary}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت سبد خرید.'}

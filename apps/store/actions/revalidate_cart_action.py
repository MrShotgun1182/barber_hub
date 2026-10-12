from customers import models as customers_models
from store import services as store_services


def RevalidateCartAction(user, displayed_prices: dict = None) -> dict:
    """اکشن بازبینی سبد خرید پیش از ثبت سفارش (تغییر قیمت یا غیرقابل‌سفارش شدن)"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        result = store_services.RevalidateCartService(
            customer, displayed_prices=displayed_prices
        )
        return {'status': 'success', 'message': '', **result}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except Exception:
        return {'status': 'error', 'message': 'خطا در بازبینی سبد خرید.'}

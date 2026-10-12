from customers import models as customers_models
from store import services as store_services


def AddToCartAction(user, product_id: int, quantity: int = 1) -> dict:
    """اکشن افزودن محصول به سبد خرید مشتری"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        store_services.AddToCartService(customer, product_id, quantity=quantity)
        return {'status': 'success', 'message': 'محصول به سبد خرید اضافه شد.'}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در افزودن محصول به سبد خرید.'}

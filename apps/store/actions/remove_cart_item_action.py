from customers import models as customers_models
from store import services as store_services


def RemoveCartItemAction(user, item_id: int) -> dict:
    """اکشن حذف یک قلم از سبد خرید"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        store_services.RemoveCartItemService(customer, item_id)
        return {'status': 'success', 'message': 'قلم مورد نظر از سبد حذف شد.'}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در حذف قلم سبد خرید.'}

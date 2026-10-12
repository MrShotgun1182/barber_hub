from customers import models as customers_models
from store import services as store_services


def UpdateCartItemAction(user, item_id: int, quantity: int) -> dict:
    """اکشن به‌روزرسانی تعداد یک قلم از سبد خرید"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)
        item = store_services.UpdateCartItemService(customer, item_id, quantity)
        if item is None:
            return {'status': 'success', 'message': 'قلم مورد نظر از سبد حذف شد.'}
        return {'status': 'success', 'message': 'تعداد به‌روزرسانی شد.'}
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در به‌روزرسانی سبد خرید.'}

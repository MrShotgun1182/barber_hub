from store import models as store_models
from store.services.get_or_create_cart_service import GetOrCreateCartService


def UpdateCartItemService(customer, item_id: int, quantity: int) -> store_models.CartItemModel:
    """تغییر تعداد یک آیتم سبد خرید (تعداد صفر باعث حذف آیتم می‌شود)"""
    if quantity < 0:
        raise ValueError('تعداد نمی‌تواند منفی باشد.')

    cart = GetOrCreateCartService(customer)

    try:
        item = store_models.CartItemModel.objects.get(id=item_id, cart=cart)
    except store_models.CartItemModel.DoesNotExist:
        raise ValueError('آیتم مورد نظر در سبد خرید شما یافت نشد.')

    if quantity == 0:
        item.delete()
        return None

    item.quantity = quantity
    item.save(update_fields=['quantity'])
    return item

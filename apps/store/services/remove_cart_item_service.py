from store import models as store_models
from store.services.get_or_create_cart_service import GetOrCreateCartService


def RemoveCartItemService(customer, item_id: int) -> None:
    """حذف یک آیتم از سبد خرید مشتری"""
    cart = GetOrCreateCartService(customer)

    try:
        item = store_models.CartItemModel.objects.get(id=item_id, cart=cart)
    except store_models.CartItemModel.DoesNotExist:
        raise ValueError('آیتم مورد نظر در سبد خرید شما یافت نشد.')

    item.delete()

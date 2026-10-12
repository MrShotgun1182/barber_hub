from store import models as store_models


def GetOrCreateCartService(customer) -> store_models.CartModel:
    """دریافت یا ساخت سبد خرید مشتری (سبد حتی پس از خروج باقی می‌ماند)"""
    cart, _ = store_models.CartModel.objects.get_or_create(customer=customer)
    return cart

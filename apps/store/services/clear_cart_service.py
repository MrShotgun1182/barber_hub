from store import models as store_models


def ClearCartService(cart) -> None:
    """پاک‌کردن همه آیتم‌های سبد خرید"""
    cart.items.all().delete()

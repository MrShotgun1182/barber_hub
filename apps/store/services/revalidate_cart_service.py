from store.services.get_cart_summary_service import GetCartSummaryService


def RevalidateCartService(customer, displayed_prices: dict = None) -> dict:
    """بازبینی مجدد قیمت و قابلیت سفارش همه آیتم‌های سبد پیش از ثبت سفارش"""
    summary = GetCartSummaryService(customer)
    displayed_prices = displayed_prices or {}

    # ۱. بررسی وضعیت انتشار/سفارش و تغییر قیمت هر محصول نسبت به مرجع
    changes = []
    blocked = False
    for row in summary['items']:
        # انتشار: محصول حذف‌شده از فروشگاه باید کاملاً از سبد خارج شود
        if not row['is_published']:
            changes.append({
                'item_id': row['item_id'],
                'product_id': row['product_id'],
                'product_title': row['product_title'],
                'change_type': 'not_published',
                'message': f"محصول «{row['product_title']}» دیگر در فروشگاه عرضه نمی‌شود و باید از سبد حذف شود.",
            })
            blocked = True
            continue

        # قابل سفارش بودن: در GetCartSummaryService بر اساس داده زنده محاسبه شده است
        if not row['is_orderable']:
            changes.append({
                'item_id': row['item_id'],
                'product_id': row['product_id'],
                'product_title': row['product_title'],
                'change_type': 'not_orderable',
                'message': f"محصول «{row['product_title']}» در حال حاضر قابل سفارش نیست و باید از سبد حذف شود.",
            })
            blocked = True
            continue

        # قیمت مرجع: قیمت نمایش‌داده‌شده در صفحه تسویه، وگرنه قیمت هنگام افزودن به سبد
        old_price = displayed_prices.get(str(row['product_id']))
        if old_price is None:
            old_price = row['cart_unit_price']
        if old_price is not None and old_price != row['unit_price']:
            changes.append({
                'item_id': row['item_id'],
                'product_id': row['product_id'],
                'product_title': row['product_title'],
                'change_type': 'price_changed',
                'old_price': old_price,
                'new_price': row['unit_price'],
                'message': f"قیمت «{row['product_title']}» تغییر کرده است.",
            })

    return {
        'items': summary['items'],
        'total': summary['total'],
        'changes': changes,
        'blocked': blocked,
    }

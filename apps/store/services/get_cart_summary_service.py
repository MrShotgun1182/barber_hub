from store.services.get_or_create_cart_service import GetOrCreateCartService


def GetCartSummaryService(customer) -> dict:
    """جمع‌بندی سبد خرید: آیتم‌ها با قیمت جاری و مجموع کل"""
    cart = GetOrCreateCartService(customer)
    items = list(
        cart.items.select_related('product', 'product__category')
    )

    item_rows = []
    total = 0
    for item in items:
        line_total = item.product.price * item.quantity
        total += line_total
        item_rows.append({
            'item_id': item.id,
            'product_id': item.product.id,
            'product_title': item.product.title,
            'unit_price': item.product.price,
            'cart_unit_price': item.unit_price,
            'quantity': item.quantity,
            'line_total': line_total,
            'is_published': item.product.is_published and not item.product.is_deleted,
            'is_orderable': (
                item.product.is_published
                and not item.product.is_deleted
                and item.product.is_orderable
            ),
        })

    return {
        'items': item_rows,
        'total': total,
        'items_count': len(item_rows),
    }

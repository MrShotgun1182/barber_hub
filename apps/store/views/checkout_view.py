import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from store import actions


@login_required
def CheckoutView(request):
    """ویوی صفحه بازبینی و تأیید نهایی سبد خرید قبل از پرداخت"""
    data = actions.GetCartAction(request.user)

    if data['status'] == 'error':
        context = {'error_message': data['message']}
        return render(request, 'store/cart.html', context)

    # کلید ایدمپوتنسی برای جلوگیری از ثبت تکراری سفارش؛ یک‌بار در session ساخته می‌شود
    if 'store_idempotency_key' not in request.session:
        request.session['store_idempotency_key'] = str(uuid.uuid4())

    # قیمت‌های نمایش‌داده‌شده در همین صفحه؛ مبنای تشخیص تغییر قیمت هنگام ثبت نهایی
    request.session['store_displayed_prices'] = {
        str(item['product_id']): item['unit_price']
        for item in data.get('items', [])
    }

    context = {
        'items': data.get('items', []),
        'total': data.get('total', 0),
        'items_count': data.get('items_count', 0),
        'customer_note': request.session.get('store_customer_note', ''),
    }
    return render(request, 'store/checkout.html', context)

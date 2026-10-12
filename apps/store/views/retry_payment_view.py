from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from store import actions


@login_required
def RetryPaymentView(request, order_id: int):
    """ویوی تلاش مجدد پرداخت سفارش در انتظار پرداخت"""
    data = actions.GetCustomerOrderDetailAction(request.user, order_id)

    if data['status'] == 'error':
        messages.error(request, data['message'])
        return redirect('store:order_history')

    order = data['order']

    # فقط سفارش‌های در انتظار پرداخت قابل تلاش مجدد هستند
    if order.status != 'PENDING_PAYMENT':
        messages.error(request, 'این سفارش در انتظار پرداخت نیست.')
        return redirect('store:order_detail', order_id=order.id)

    payment_data = actions.InitiatePaymentAction(order)
    if payment_data['status'] == 'success':
        return redirect(payment_data['payment_url'])

    messages.error(request, payment_data['message'])
    return redirect('store:order_detail', order_id=order.id)

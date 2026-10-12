from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from store import actions


def PaymentCallbackView(request):
    """ویوی بازگشت از درگاه پرداخت زرین‌پال؛ بدون login_required چون درگاه ناشناس برمی‌گرداند"""
    authority = request.GET.get('Authority', '')
    gateway_status = request.GET.get('Status', '')

    if not authority:
        return redirect('store:store_home')

    data = actions.VerifyPaymentAction(authority, gateway_status)

    order = data.get('order')
    if order is None:
        return render(
            request,
            'store/payment_result.html',
            {'status': 'error', 'message': data.get('message', '')},
        )

    return redirect(
        reverse('store:payment_result', kwargs={'order_id': order.id})
        + f'?status={data["status"]}'
    )


@login_required
def PaymentResultView(request, order_id: int):
    """ویوی صفحه نتیجه پرداخت سفارش"""
    data = actions.GetCustomerOrderDetailAction(request.user, order_id)
    if data['status'] == 'error':
        return render(
            request,
            'store/payment_result.html',
            {'status': 'error', 'message': data['message']},
        )

    query_status = request.GET.get('status', '')
    context = {
        'order': data['order'],
        'items': data.get('items', []),
        'payments': data.get('payments', []),
        'query_status': query_status,
    }
    return render(request, 'store/payment_result.html', context)

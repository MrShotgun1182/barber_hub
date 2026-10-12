from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from store import actions


@login_required
def OrderDetailView(request, order_id: int):
    """ویوی جزئیات یک سفارش مشتری"""
    data = actions.GetCustomerOrderDetailAction(request.user, order_id)

    if data['status'] == 'error':
        context = {'error_message': data['message']}
        return render(request, 'store/order_not_found.html', context, status=404)

    context = {
        'order': data['order'],
        'items': data.get('items', []),
        'payments': data.get('payments', []),
    }
    return render(request, 'store/order_detail.html', context)

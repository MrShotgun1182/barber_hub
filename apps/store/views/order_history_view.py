from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from store import actions


@login_required
def OrderHistoryView(request):
    """ویوی تاریخچه سفارش‌های مشتری"""
    data = actions.GetCustomerOrdersAction(request.user)

    context = {
        'orders': data.get('orders', []),
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'store/order_history.html', context)

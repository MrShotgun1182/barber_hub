from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from store import actions


@login_required
def CartView(request):
    """ویوی صفحه سبد خرید مشتری"""
    data = actions.GetCartAction(request.user)

    context = {
        'items': data.get('items', []),
        'total': data.get('total', 0),
        'items_count': data.get('items_count', 0),
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'store/cart.html', context)

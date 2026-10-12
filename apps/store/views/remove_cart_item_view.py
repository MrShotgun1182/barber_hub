from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from store import actions


@login_required
@require_POST
def RemoveCartItemView(request, item_id: int):
    """ویوی حذف یک قلم از سبد خرید (فقط AJAX/JSON)"""
    data = actions.RemoveCartItemAction(request.user, item_id)
    if data['status'] == 'success':
        summary = actions.GetCartAction(request.user)
        data['total'] = summary.get('total', 0)
        data['items_count'] = summary.get('items_count', 0)
    return JsonResponse(data, status=200 if data['status'] != 'error' else 400)

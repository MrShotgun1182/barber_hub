import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from store import actions


@login_required
@require_POST
def UpdateCartItemView(request, item_id: int):
    """ویوی به‌روزرسانی تعداد یک قلم سبد خرید (فقط AJAX/JSON)"""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400
        )

    quantity = payload.get('quantity')

    if not isinstance(quantity, int) or quantity < 0:
        return JsonResponse(
            {'status': 'error', 'message': 'تعداد نامعتبر است.'}, status=400
        )

    data = actions.UpdateCartItemAction(request.user, item_id, quantity)
    # برای به‌روزرسانی جمع کل صفحه، جمع‌بندی تازه را هم برمی‌گردانیم
    if data['status'] == 'success':
        summary = actions.GetCartAction(request.user)
        data['total'] = summary.get('total', 0)
        data['items_count'] = summary.get('items_count', 0)
    return JsonResponse(data, status=200 if data['status'] != 'error' else 400)

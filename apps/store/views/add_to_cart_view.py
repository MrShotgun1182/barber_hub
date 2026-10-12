import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from store import actions


@login_required
@require_POST
def AddToCartView(request):
    """ویوی افزودن محصول به سبد خرید (فقط AJAX/JSON)"""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400
        )

    product_id = payload.get('product_id')
    quantity = payload.get('quantity', 1)

    if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity < 1:
        return JsonResponse(
            {'status': 'error', 'message': 'شناسه محصول یا تعداد نامعتبر است.'},
            status=400,
        )

    data = actions.AddToCartAction(request.user, product_id, quantity=quantity)
    return JsonResponse(data, status=200 if data['status'] != 'error' else 400)

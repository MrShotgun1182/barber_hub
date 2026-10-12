import json
import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from store import actions


@login_required
@require_POST
def SubmitCheckoutView(request):
    """ویوی ثبت نهایی سفارش (فقط AJAX/JSON)؛ در صورت موفقیت آدرس پرداخت را برمی‌گرداند"""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400
        )

    idempotency_key = request.session.get('store_idempotency_key')
    if not idempotency_key:
        return JsonResponse(
            {'status': 'error', 'message': 'نشست شما منقضی شده است. دوباره تلاش کنید.'},
            status=400,
        )

    confirm_changes = payload.get('confirm_changes') is True
    customer_note = payload.get('customer_note', '')
    if not isinstance(customer_note, str):
        customer_note = ''

    data = actions.SubmitCheckoutAction(
        request.user,
        idempotency_key=idempotency_key,
        confirm_changes=confirm_changes,
        customer_note=customer_note,
        displayed_prices=request.session.get('store_displayed_prices'),
    )

    # سفارش (چه تازه چه بازپخش) → آغاز پرداخت و آدرس درگاه
    if data['status'] == 'success':
        request.session['store_customer_note'] = customer_note
        payment_data = actions.InitiatePaymentAction(data['order'])
        if payment_data['status'] == 'success':
            # کلید نو برای سفارش بعدی و پاک‌سازی قیمت‌های نمایش‌داده‌شده
            request.session['store_idempotency_key'] = str(uuid.uuid4())
            request.session.pop('store_displayed_prices', None)
            return JsonResponse(
                {
                    'status': 'success',
                    'message': data['message'],
                    'order_id': data['order'].id,
                    'order_number': data['order'].order_number,
                    'payment_url': payment_data['payment_url'],
                }
            )
        # سفارش ثبت شد اما درگاه پاسخ نداد؛ کاربر می‌تواند از تاریخچه تلاش مجدد کند
        return JsonResponse(
            {
                'status': 'success',
                'message': data['message'] + ' اما ارتباط با درگاه برقرار نشد؛ می‌توانید از تاریخچه سفارش‌ها پرداخت را مجدد تلاش کنید.',
                'order_id': data['order'].id,
                'order_number': data['order'].order_number,
                'payment_url': None,
            }
        )

    # تغییر قیمت → نیاز به تأیید مشتری
    if data['status'] == 'needs_confirmation':
        return JsonResponse(data)

    return JsonResponse(data, status=400)

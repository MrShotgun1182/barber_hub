import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from OTP import actions


@require_POST
def SendOTPView(request):
    """ویو دریافت شماره موبایل و ارسال کد OTP"""
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')

        if not phone_number or len(phone_number) != 11:
            return JsonResponse(
                {'status': 'error', 'message': 'شماره موبایل معتبر نیست'},
                status=400,
            )

        result = actions.SendOTPAction(phone_number)
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'فرمت داده ارسال‌شده اشتباه است'},
            status=400,
        )
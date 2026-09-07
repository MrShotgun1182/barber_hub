import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from OTP import actions 


@require_POST
def VerifyOTPView(request):
    """ویو تایید کد OTP و ورود کاربر"""
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code')

        if not phone_number or not otp_code:
            return JsonResponse(
                {'status': 'error', 'message': 'اطلاعات ورودی کامل نیست'},
                status=400,
            )

        result = actions.VerifyOTPAction(request, phone_number, otp_code)
        status_code = 200 if result['is_authenticated'] else 400
        return JsonResponse(result, status=status_code)

    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'فرمت داده ارسال‌شده اشتباه است'},
            status=400,
        )
from django.contrib.auth import login
from OTP import services as OTP_services
from accounts import services as accounts_services

def VerifyOTPAction(request, phone_number: str, otp_code: str) -> dict:
    """اکشن تایید OTP و احراز هویت نهایی کاربر"""
    # ۱. اعتبارسنجی کد
    if not OTP_services.VerifyOTPCodeService(phone_number, otp_code):
        return {
            'status': 'error',
            'message': 'کد تایید نامعتبر یا منقضی شده است',
            'is_authenticated': False
        }

    # ۲. دریافت یا ساخت کاربر و پروفایل
    user, _ = accounts_services.GetOrCreateUserByPhoneService(phone_number)

    # ۳. احراز هویت و ایجاد Session
    login(request, user)

    return {
        'status': 'success',
        'message': 'کد با موفقیت تایید شد',
        'is_authenticated': True
    }
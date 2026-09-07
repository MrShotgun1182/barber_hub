from OTP import models

def VerifyOTPCodeService(phone_number: str, code: str) -> bool:
    """بررسی صحت و انقضای کد OTP"""
    otp = models.OTPModel.objects.filter(
        phone_number=phone_number,
        code=code,
        is_used=False
    ).first()

    if otp and otp.is_valid(expiry_minutes=2):
        otp.is_used = True
        otp.save()
        return True
    return False
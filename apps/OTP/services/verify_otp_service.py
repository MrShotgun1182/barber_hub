from django.db import transaction
from OTP import models


def VerifyOTPCodeService(phone_number: str, code: str) -> bool:
    """
    بررسی صحت و انقضای کد OTP با محافظت در برابر brute-force.

    - فقط آخرین کد فعال هر شماره بررسی می‌شود.
    - هر تلاش ناموفق شمارنده‌ی attempts را افزایش می‌دهد.
    - پس از رسیدن به سقف تلاش، کد باطل (is_used=True) می‌شود.
    """
    with transaction.atomic():
        otp = (
            models.OTPModel.objects.select_for_update()
            .filter(phone_number=phone_number, is_used=False)
            .order_by('-created_at')
            .first()
        )

        if otp is None or otp.is_locked:
            return False

        # مقایسه‌ی امن کد دریافتی با کد ذخیره‌شده
        if not otp.is_valid(expiry_minutes=2) or otp.code != code:
            otp.attempts += 1
            # در صورت رسیدن به سقف، کد برای همیشه باطل می‌شود
            if otp.attempts >= models.OTPModel.MAX_ATTEMPTS:
                otp.is_used = True
            otp.save(update_fields=['attempts', 'is_used'])
            return False

        # کد صحیح: مصرف و باطل می‌شود
        otp.is_used = True
        otp.save(update_fields=['is_used'])
        return True
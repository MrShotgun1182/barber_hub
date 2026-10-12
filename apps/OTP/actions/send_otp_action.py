import logging

from django.db import transaction
from OTP import models, services, tasks

logger = logging.getLogger(__name__)


def SendOTPAction(phone_number: str) -> dict:
    """اکشن مدیریت فرآیند درخواست و ارسال کد OTP"""
    # ۱. تولید کد
    code = services.GenerateOTPCodeService(length=6)

    with transaction.atomic():
        # ۲. باطل کردن کدهای فعال قبلی همین شماره (جلوگیری از چند کد فعال هم‌زمان)
        models.OTPModel.objects.filter(
            phone_number=phone_number, is_used=False
        ).update(is_used=True)

        # ۳. ثبت کد جدید در دیتابیس
        otp = models.OTPModel.objects.create(
            phone_number=phone_number,
            code=code,
        )

    # ۴. ارسال غیرهمزمان با Celery (در صورت خرابی بروکر، نتیجه واقعی برگردانده می‌شود)
    try:
        tasks.SendOTPSMSTask.delay(phone_number, code)
    except Exception:
        logger.exception('صف‌بندی ارسال پیامک OTP با خطا مواجه شد')
        # کد ثبت‌شده بلااستفاده می‌ماد؛ آن را باطل می‌کنیم
        models.OTPModel.objects.filter(id=otp.id).update(is_used=True)
        return {
            'status': 'error',
            'message': 'ارسال پیامک با خطا مواجه شد. لطفاً مجدداً تلاش کنید.',
        }

    return {
        'status': 'success',
        'message': 'کد تایید با موفقیت ارسال شد',
    }
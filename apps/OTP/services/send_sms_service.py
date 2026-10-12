import logging

from django.conf import settings
from melipayamak import Api

logger = logging.getLogger(__name__)


def SendSMSService(to_phone: str, text: str) -> bool:
    """
    ارسال پیامک با استفاده از پکیج رسمی ملی‌پیامک

    در صورت موفقیت True و در غیر این صورت False برمی‌گرداند.
    """
    try:
        # گرفتن اطلاعات اکانت از تنظیمات پروژه
        username = settings.MELIPAYAMAK_USERNAME
        password = settings.MELIPAYAMAK_PASSWORD
        _from = settings.MELIPAYAMAK_FROM

        # راه‌اندازی کلاس API
        api = Api(username, password)
        sms = api.sms()

        # ارسال پیامک
        response = sms.send(to_phone, _from, text)

        # پکیج ملی‌پیامک نتیجه را در کلید RecId برمی‌گرداند؛
        # مقدار khoshgolab یا RetStatus=-1 نشانه‌ی خطاست.
        if isinstance(response, dict):
            if response.get('RetStatus') == -1 or response.get('Value') == 'khoshgolab':
                logger.error('خطای ارسال پیامک ملی‌پیامک: %s', response)
                return False
            return bool(response.get('RecId'))

        return bool(response)

    except Exception:
        logger.exception('خطای غیرمنتظره در ارسال پیامک')
        return False
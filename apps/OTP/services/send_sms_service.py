from django.conf import settings
from melipayamak import Api

def SendSMSService(to_phone: str, text: str) -> bool:
    """
    ارسال پیامک با استفاده از پکیج رسمی ملی‌پیامک
    """
    try:
        # گرفتن اطلاعات اکانت از تنظیمات پروژه
        username = settings.MELIPAYAMAK_USERNAME
        password = settings.MELIPAYAMAK_PASSWORD
        _from = settings.MELIPAYAMAK_FROM

        print(username, password)
        
        # راه‌اندازی کلاس API
        api = Api(username, password)
        sms = api.sms()
        
        # ارسال پیامک
        response = sms.send(to_phone, _from, text)
        
        print("=== DEBUG MeliPayamak Package ===")
        print("Response:", response)
        print("=================================")
        
        # معمولا اگر ارسال موفق باشه، یک دیکشنری یا رشته حاوی کد پیگیری (RecId) برمی‌گرده
        # اگر خطا بده داخل همون response مشخص میشه
        if response:
            return True
        return False
        
    except Exception as e:
        print("MeliPayamak Package Error:", e)
        return False
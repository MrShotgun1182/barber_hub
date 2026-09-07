import requests
from django.conf import settings

def SendSMSService(to_phone: str, text: str) -> bool:
    """ارسال مستقیم پیامک از طریق وب‌سرویس REST ملی پیامک"""
    url = "http://api.payamak-panel.com/post/Send.asmx/SendSimpleSMS2"
    payload = {
        'username': settings.MELIPAYAMAK_USERNAME,
        'password': settings.MELIPAYAMAK_PASSWORD,
        'from': settings.MELIPAYAMAK_FROM,
        'to': to_phone,
        'text': text,
        'isflash': False
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False
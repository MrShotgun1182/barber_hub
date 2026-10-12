import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

ZARINPAL_VERIFY_PATH = '/pg/v4/payment/verify.json'


def _GetBaseURL() -> str:
    """انتخاب آدرس پایه درگاه بر اساس حالت sandbox یا پروداکشن"""
    if settings.ZARINPAL_SANDBOX:
        return 'https://sandbox.zarinpal.com'
    return 'https://payment.zarinpal.com'


def ZarinPalVerifyService(payment, authority: str) -> dict:
    """تأیید تراکنش پرداخت نزد زرین‌پال (خروجی dict؛ خطای درگاه exception نمی‌دهد)"""
    url = _GetBaseURL() + ZARINPAL_VERIFY_PATH

    payload = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': payment.amount,
        'currency': settings.ZARINPAL_CURRENCY,
        'authority': authority,
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        body = response.json()
    except (requests.RequestException, ValueError):
        logger.exception('خطای ارتباط با درگاه پرداخت زرین‌پال در تأیید')
        raise ValueError('ارتباط با درگاه پرداخت برقرار نشد.')

    data = body.get('data') or {}
    code = data.get('code')

    if code == 100:
        # تراکنش با موفقیت تأیید شد
        return {'status': 'verified', 'ref_id': str(data.get('ref_id', '')), 'code': 100}

    if code == 101:
        # تراکنش قبلاً تأیید شده است (بازپخش ایدمپوتنت)
        return {'status': 'verified', 'ref_id': str(data.get('ref_id', '') or payment.ref_id or ''), 'code': 101}

    # سایر کدها: پرداخت ناموفق
    logger.error('خطای تأیید پرداخت زرین‌پال: %s', body)
    return {'status': 'failed', 'code': code, 'message': 'پرداخت تأیید نشد.'}

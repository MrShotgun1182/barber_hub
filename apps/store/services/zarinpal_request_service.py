import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# سکشن انتهایی درگاه: request یا verify
ZARINPAL_REQUEST_PATH = '/pg/v4/payment/request.json'


def _GetBaseURL() -> str:
    """انتخاب آدرس پایه درگاه بر اساس حالت sandbox یا پروداکشن"""
    if settings.ZARINPAL_SANDBOX:
        return 'https://sandbox.zarinpal.com'
    return 'https://payment.zarinpal.com'


def ZarinPalRequestService(payment) -> dict:
    """ارسال درخواست پرداخت به زرین‌پال و دریافت شناسه تراکنش و لینک پرداخت"""
    url = _GetBaseURL() + ZARINPAL_REQUEST_PATH

    payload = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': payment.amount,
        'currency': settings.ZARINPAL_CURRENCY,
        'description': f'سفارش {payment.order.order_number} - باربر هاب',
        'callback_url': settings.ZARINPAL_CALLBACK_URL,
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        body = response.json()
    except (requests.RequestException, ValueError):
        logger.exception('خطای ارتباط با درگاه پرداخت زرین‌پال')
        raise ValueError('ارتباط با درگاه پرداخت برقرار نشد.')

    data = body.get('data') or {}
    if data.get('code') == 100:
        authority = data['authority']
        payment_url = f"{_GetBaseURL()}/pg/StartPay/{authority}"
        return {'authority': authority, 'payment_url': payment_url}

    # خطای درگاه: ثبت لاگ و بازگرداندن پیام فارسی
    errors = body.get('errors') or {}
    logger.error('خطای درگاه زرین‌پال در درخواست پرداخت: %s', body)
    raise ValueError(f"درگاه پرداخت درخواست را نپذیرفت. (کد {errors.get('code', 'نامشخص')})")

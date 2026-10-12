from django.db import transaction

from store import services as store_services


def VerifyPaymentAction(authority: str, gateway_status: str) -> dict:
    """اکشن تأیید پرداخت پس از بازگشت از درگاه؛ ایدمپوتنت و مقاوم به callback تکراری"""
    try:
        # ۱. بازگشت ناموفق از درگاه → پرداخت لغو می‌شود؛ سفارش در انتظار می‌ماند و تلاش مجدد ممکن است
        if gateway_status != 'OK':
            with transaction.atomic():
                payment = store_services.GetPaymentByAuthorityService(authority)
                if payment is None:
                    return {'status': 'error', 'message': 'پرداخت یافت نشد.'}
                if payment.status == 'VERIFIED':
                    return {
                        'status': 'success',
                        'message': 'این پرداخت قبلاً تأیید شده است.',
                        'order': payment.order,
                    }
                store_services.MarkPaymentCancelledService(payment)
            return {
                'status': 'error',
                'message': 'پرداخت توسط شما لغو شد یا ناموفق بود.',
                'order': payment.order,
            }

        # ۲. قفل رکورد پرداخت تا callbackهای همزمان سریالی شوند
        with transaction.atomic():
            payment = store_services.GetPaymentByAuthorityService(authority)
            if payment is None:
                return {'status': 'error', 'message': 'پرداخت یافت نشد.'}

            # ۳. اگر قبلاً تأیید شده، بدون تماس مجدد با درگاه موفق را برگردان
            if payment.status == 'VERIFIED':
                return {
                    'status': 'success',
                    'message': 'این پرداخت قبلاً تأیید شده است.',
                    'order': payment.order,
                }

            # ۴. تأیید نهایی نزد درگاه (داخل قفل — فقط یک‌بار برای هر authority)
            result = store_services.ZarinPalVerifyService(payment, authority)

            if result['status'] == 'verified':
                store_services.MarkPaymentVerifiedService(
                    payment, ref_id=result['ref_id'], code=result['code']
                )
                # ۵. سفارش فقط با تأیید پرداخت به «ثبت‌شده» می‌رود
                if payment.order.status == 'PENDING_PAYMENT':
                    store_services.UpdateOrderStatusService(payment.order, 'PLACED')
                return {
                    'status': 'success',
                    'message': 'پرداخت با موفقیت تأیید شد.',
                    'order': payment.order,
                    'ref_id': result['ref_id'],
                }

            # ۶. تأیید نشد → پرداخت ناموفق؛ سفارش در انتظار پرداخت می‌ماند
            store_services.MarkPaymentFailedService(
                payment, code=result.get('code'), message=result.get('message', '')
            )
            return {
                'status': 'error',
                'message': result.get('message', 'پرداخت تأیید نشد.'),
                'order': payment.order,
            }
    except Exception:
        return {'status': 'error', 'message': 'خطا در تأیید پرداخت.'}

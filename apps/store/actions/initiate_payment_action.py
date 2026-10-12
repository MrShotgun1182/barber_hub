from store import services as store_services


def InitiatePaymentAction(order) -> dict:
    """اکشن آغاز پرداخت سفارش از طریق درگاه زرین‌پال"""
    try:
        # ۱. ساخت رکورد پرداخت (هر تلاش، یک رکورد جدید با authority جدید)
        payment = store_services.CreatePaymentService(order)

        # ۲. درخواست به درگاه
        result = store_services.ZarinPalRequestService(payment)

        # ۳. ذخیره authority دریافتی
        store_services.SetPaymentAuthorityService(payment, result['authority'])

        return {
            'status': 'success',
            'message': 'پرداخت آغاز شد.',
            'payment': payment,
            'payment_url': result['payment_url'],
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در آغاز پرداخت. مجدداً تلاش کنید.'}

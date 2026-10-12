from customers import models as customers_models
from store import services as store_services


def SubmitCheckoutAction(
    user,
    idempotency_key: str,
    confirm_changes: bool = False,
    customer_note: str = '',
    displayed_prices: dict = None,
) -> dict:
    """اکشن ثبت نهایی سفارش از سبد خرید؛ با بازبینی قیمت‌ها و کلید ایدمپوتنسی"""
    try:
        customer = customers_models.CustomerModel.objects.get(user=user)

        # ۱. اگر سفارشی با همین کلید قبلاً ثبت شده، همان را بازپخش کن (ثبت تکراری نداریم)
        existing_order = store_services.GetOrderByIdempotencyKeyService(idempotency_key)
        if existing_order is not None:
            return {
                'status': 'success',
                'message': 'سفارش شما قبلاً ثبت شده است.',
                'order': existing_order,
                'already_exists': True,
            }

        # ۲. بازبینی سبد: اگر قلم غیرقابل‌سفارشی هست، ادامه ممکن نیست
        # ۳. اگر تغییری در قیمت‌ها هست و مشتری هنوز تأیید نکرده، نیاز به تأیید دارد
        if not confirm_changes:
            revalidation = store_services.RevalidateCartService(
                customer, displayed_prices=displayed_prices
            )
            if revalidation['blocked']:
                return {
                    'status': 'error',
                    'message': 'برخی اقلام سبد شما دیگر قابل سفارش نیستند. لطفاً آن‌ها را حذف کنید.',
                    'changes': revalidation['changes'],
                }
            if revalidation['changes']:
                return {
                    'status': 'needs_confirmation',
                    'message': 'قیمت یا وضعیت برخی اقلام تغییر کرده است.',
                    'changes': revalidation['changes'],
                    'total': revalidation['total'],
                }

        # ۴. ثبت اتمیک سفارش با قیمت‌های تازه‌خوانده‌شده (نه قیمت‌های صفحه قبل)
        order = store_services.CreateOrderService(
            customer,
            idempotency_key=idempotency_key,
            customer_note=customer_note,
        )

        return {
            'status': 'success',
            'message': 'سفارش شما با موفقیت ثبت شد.',
            'order': order,
            'already_exists': False,
        }
    except customers_models.CustomerModel.DoesNotExist:
        return {'status': 'error', 'message': 'پروفایل مشتری یافت نشد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در ثبت سفارش. مجدداً تلاش کنید.'}

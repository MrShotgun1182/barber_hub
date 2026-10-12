from django.db import transaction, IntegrityError
from store import models as store_models
from store.services.generate_order_number_service import GenerateOrderNumberService
from store.services.get_or_create_cart_service import GetOrCreateCartService


def CreateOrderService(customer, idempotency_key: str = None, customer_note: str = '') -> store_models.OrderModel:
    """ساخت اتمیک سفارش همراه با اسنپ‌شات قیمت‌ها و پاک‌شدن سبد خرید"""
    with transaction.atomic():
        # ۱. دریافت سبد و قفل آن برای جلوگیری از تغییر هم‌زمان
        cart = GetOrCreateCartService(customer)
        items = list(
            cart.items.select_related('product')
        )
        if not items:
            raise ValueError('سبد خرید شما خالی است.')

        # ۲. بررسی قابل سفارش بودن همه محصولات (قیمت‌ها از داده زنده اسنپ‌شات می‌شوند)
        for item in items:
            if not (item.product.is_published and not item.product.is_deleted and item.product.is_orderable):
                raise ValueError(f"محصول «{item.product.title}» در حال حاضر قابل سفارش نیست.")

        # ۳. محاسبه مبلغ کل از قیمت‌های جاری
        total_amount = sum(item.product.price * item.quantity for item in items)

        # ۴. ساخت سفارش با شماره یکتا (با تلاش مجدد در صورت تصادم)
        order = None
        for _ in range(5):
            try:
                order = store_models.OrderModel.objects.create(
                    order_number=GenerateOrderNumberService(),
                    customer=customer,
                    status='PENDING_PAYMENT',
                    total_amount=total_amount,
                    customer_full_name=(
                        f"{customer.user.first_name} {customer.user.last_name}".strip()
                    ),
                    customer_phone=customer.user.phone_number or '',
                    customer_note=customer_note or '',
                    idempotency_key=idempotency_key,
                )
                break
            except IntegrityError:
                # تصادم روی idempotency_key یعنی سفارش قبلاً ثبت شده است
                if idempotency_key:
                    existing = store_models.OrderModel.objects.filter(
                        idempotency_key=idempotency_key
                    ).first()
                    if existing:
                        return existing
                continue

        if order is None:
            raise ValueError('خطا در ثبت شماره سفارش. مجدداً تلاش کنید.')

        # ۵. ثبت آیتم‌های سفارش با اسنپ‌شات قیمت در زمان خرید
        for item in items:
            store_models.OrderItemModel.objects.create(
                order=order,
                product=item.product,
                product_title=item.product.title,
                unit_price=item.product.price,
                quantity=item.quantity,
                line_total=item.product.price * item.quantity,
            )

        # ۶. پاک‌کردن سبد خرید پس از ثبت موفق
        cart.items.all().delete()

        return order

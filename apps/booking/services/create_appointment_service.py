from datetime import datetime
from django.db import transaction
from booking import models as booking_models
from barbers import models as barbers_models
from customers import models as customers_models


def CreateAppointmentService(
    user,
    barber_id: int,
    barber_service_ids: list[int],
    booking_date: str,
    start_time_str: str,
    end_time_str: str,
) -> booking_models.AppointmentModel:
    """
    ثبت اتمیک نوبت رزرو به همراه بررسی صحت داده‌ها و محاسبه قیمت کل
    """
    with transaction.atomic():
        # ۱. دریافت یا ایجاد پروفایل مشتری
        customer, _ = customers_models.CustomerModel.objects.get_or_create(user=user)

        # ۲. اعتبارسنجی آرایشگر و خدمات
        barber = barbers_models.BarberModel.objects.get(id=barber_id, is_active=True)
        barber_services = list(
            barbers_models.BarberServiceModel.objects.filter(
                id__in=barber_service_ids, barber=barber, is_active=True
            ).select_related('service')
        )

        if not barber_services:
            raise ValueError('هیچ خدمت معتبری انتخاب نشده است.')

        # ۳. محاسبه مجموع قیمت و زمان
        total_price = sum(
            s.custom_price
            if s.custom_price is not None
            else s.service.base_price
            for s in barber_services
        )
        total_duration = sum(
            s.custom_duration_minutes
            if s.custom_duration_minutes is not None
            else s.service.default_duration_minutes
            for s in barber_services
        )

        # ۴. تبدیل استرینگ‌ها به Object زمان و تاریخ
        date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
        start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()

        # ۵. بررسی مجدد تداخل زمانی (جلوگیری از Double Booking در رزرو هم‌زمان)
        has_overlap = booking_models.AppointmentModel.objects.filter(
            barber=barber,
            date=date_obj,
            status__in=['PENDING', 'CONFIRMED'],
            start_time__lt=end_time_obj,
            end_time__gt=start_time_obj,
        ).exists()

        if has_overlap:
            raise ValueError(
                'متأسفانه این زمان همین چند لحظه پیش توسط شخص دیگری رزرو شد.'
            )

        # ۶. ثبت نوبت
        appointment = booking_models.AppointmentModel.objects.create(
            customer=customer,
            barber=barber,
            date=date_obj,
            start_time=start_time_obj,
            end_time=end_time_obj,
            total_price=total_price,
            total_duration_minutes=total_duration,
            status='PENDING',
        )
        appointment.services.set(barber_services)

        return appointment
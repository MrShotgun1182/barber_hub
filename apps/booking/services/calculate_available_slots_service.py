from datetime import datetime, timedelta, date
from django.utils import timezone
from barbers import models as barbers_models
from booking import models as booking_models


def CalculateAvailableSlotsService(
    barber_id: int, barber_service_ids: list[int], target_date: date
) -> list[dict]:
    """
    محاسبه پویای سانس‌های زمانی آزاد بر اساس مجموع زمان خدمات انتخاب‌شده،
    ساعات کاری آرایشگر و عدم تداخل با نوبت‌های قبلی.
    """
    # ۱. محاسبه مجموع مدت‌زمان خدمات انتخابی
    services = barbers_models.BarberServiceModel.objects.filter(
        id__in=barber_service_ids, barber_id=barber_id, is_active=True
    ).select_related('service')

    if not services.exists():
        return []

    total_duration = sum(
        s.custom_duration_minutes
        if s.custom_duration_minutes is not None
        else s.service.default_duration_minutes
        for s in services
    )

    if total_duration <= 0:
        return []

    # ۲. نگاشت روز هفته پایتون به Model (شنبه=۰ تا جمعه=۶)
    model_day_of_week = (target_date.weekday() + 2) % 7

    try:
        working_hours = barbers_models.WorkingHoursModel.objects.get(
            barber_id=barber_id,
            day_of_week=model_day_of_week,
            is_closed=False,
        )
    except barbers_models.WorkingHoursModel.DoesNotExist:
        return []  # آرایشگر در این روز تعطیل است

    # ۳. دریافت نوبت‌های فعال ثبت‌شده در این روز (جلوگیری از N+1)
    booked_appointments = list(
        booking_models.AppointmentModel.objects.filter(
            barber_id=barber_id,
            date=target_date,
            status__in=['PENDING', 'CONFIRMED'],
        ).values('start_time', 'end_time')
    )

    start_dt = datetime.combine(target_date, working_hours.start_time)
    end_dt = datetime.combine(target_date, working_hours.end_time)
    slot_step = timedelta(minutes=working_hours.slot_duration)
    service_duration = timedelta(minutes=total_duration)

    now = timezone.localtime()
    available_slots = []
    current_dt = start_dt

    # ۴. حلقه‌ی تولید اسلات‌های بدون تداخل
    while current_dt + service_duration <= end_dt:
        slot_start = current_dt.time()
        slot_end = (current_dt + service_duration).time()

        # فیلتر کردن زمان‌های گذشته اگر روز انتخابی "امروز" باشد
        if target_date == now.date() and current_dt < now.replace(tzinfo=None):
            current_dt += slot_step
            continue

        # بررسی فرمول تداخل زمان‌ها: max(start1, start2) < min(end1, end2)
        is_overlapping = any(
            max(slot_start, app['start_time']) < min(slot_end, app['end_time'])
            for app in booked_appointments
        )

        if not is_overlapping:
            available_slots.append({
                'start_time': slot_start.strftime('%H:%M'),
                'end_time': slot_end.strftime('%H:%M'),
                'display_text': f"{slot_start.strftime('%H:%M')} تا {slot_end.strftime('%H:%M')}",
            })

        current_dt += slot_step

    return available_slots
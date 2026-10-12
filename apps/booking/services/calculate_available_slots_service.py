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

    پشتیبانی از چند شیفت کاری در یک روز و محدوده‌ی زمانی اختصاصی هر خدمت.
    """
    # ۱. محاسبه مجموع مدت‌زمان خدمات انتخابی و محدوده‌ی مجاز ارائه‌ی آن‌ها
    services = list(
        barbers_models.BarberServiceModel.objects.filter(
            id__in=barber_service_ids, barber_id=barber_id, is_active=True
        ).select_related('service')
    )

    if not services:
        return []

    total_duration = sum(
        s.custom_duration_minutes
        if s.custom_duration_minutes is not None
        else s.service.default_duration_minutes
        for s in services
    )

    if total_duration <= 0:
        return []

    # محدوده‌ی زمانی مشترک خدمات انتخاب‌شده (در صورت تعیین شدن روی هر خدمت).
    # نوبت باید داخل بازه‌ی همه‌ی خدمات انتخابی جا شود، پس سخت‌گیرانه‌ترین بازه اعمال می‌شود.
    bound_starts = [s.start_time for s in services if s.start_time is not None]
    bound_ends = [s.end_time for s in services if s.end_time is not None]
    service_start_bound = max(bound_starts) if bound_starts else None
    service_end_bound = min(bound_ends) if bound_ends else None

    # ۲. نگاشت روز هفته پایتون به Model (شنبه=۰ تا جمعه=۶)
    model_day_of_week = (target_date.weekday() + 2) % 7

    # آرایشگر ممکن است در یک روز چند شیفت کاری داشته باشد (بدون unique_together)
    working_shifts = barbers_models.WorkingHoursModel.objects.filter(
        barber_id=barber_id,
        day_of_week=model_day_of_week,
        is_closed=False,
    ).order_by('start_time')

    if not working_shifts.exists():
        return []  # آرایشگر در این روز تعطیل است

    # ۳. دریافت نوبت‌های فعال ثبت‌شده در این روز (جلوگیری از N+1)
    booked_appointments = list(
        booking_models.AppointmentModel.objects.filter(
            barber_id=barber_id,
            date=target_date,
            status__in=['PENDING', 'CONFIRMED'],
        ).values('start_time', 'end_time')
    )

    now = timezone.localtime().replace(tzinfo=None)
    service_duration = timedelta(minutes=total_duration)
    available_slots = []
    seen_slots = set()

    # ۴. حلقه روی تمام شیفت‌های روز و تولید اسلات‌های بدون تداخل
    for shift in working_shifts:
        shift_start = shift.start_time
        shift_end = shift.end_time

        # اعمال محدوده‌ی اختصاصی خدمت (در صورت وجود) روی بازه‌ی شیفت
        if service_start_bound is not None:
            shift_start = max(shift_start, service_start_bound)
        if service_end_bound is not None:
            shift_end = min(shift_end, service_end_bound)

        if shift_start >= shift_end:
            continue  # بازه‌ای برای ارائه‌ی خدمت در این شیفت باقی نمی‌ماند

        start_dt = datetime.combine(target_date, shift_start)
        end_dt = datetime.combine(target_date, shift_end)
        slot_step = timedelta(minutes=shift.slot_duration)
        current_dt = start_dt

        while current_dt + service_duration <= end_dt:
            slot_start = current_dt.time()
            slot_end = (current_dt + service_duration).time()

            # فیلتر کردن زمان‌های گذشته اگر روز انتخابی "امروز" باشد
            if target_date == now.date() and current_dt < now:
                current_dt += slot_step
                continue

            # جلوگیری از تکرار اسلات در صورت هم‌پوشانی شیفت‌ها
            slot_key = (slot_start, slot_end)
            if slot_key in seen_slots:
                current_dt += slot_step
                continue

            # بررسی فرمول تداخل زمان‌ها: max(start1, start2) < min(end1, end2)
            is_overlapping = any(
                max(slot_start, app['start_time']) < min(slot_end, app['end_time'])
                for app in booked_appointments
            )

            if not is_overlapping:
                seen_slots.add(slot_key)
                available_slots.append({
                    'start_time': slot_start.strftime('%H:%M'),
                    'end_time': slot_end.strftime('%H:%M'),
                    'display_text': f"{slot_start.strftime('%H:%M')} تا {slot_end.strftime('%H:%M')}",
                })

            current_dt += slot_step

    available_slots.sort(key=lambda slot: slot['start_time'])
    return available_slots
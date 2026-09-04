from typing import List, Dict, Any
from barbers import models as barbers_models
from barbers import services as barbers_services


def GetBarberWorkingHoursDataAction(barber: barbers_models.BarberModel) -> List[Dict[str, Any]]:
    """
    دریافت و ساختاردهی برنامه کاری هفتگی آرایشگر با پشتیبانی از شیفت‌های متکثر
    """
    saved_hours = barbers_services.GetBarberWorkingHoursService(barber=barber)

    hours_by_day = {code: [] for code, _ in barbers_models.WorkingHoursModel.DAYS_OF_WEEK}
    closed_days = set()

    for wh in saved_hours:
        if wh.is_closed:
            closed_days.add(wh.day_of_week)
        else:
            hours_by_day[wh.day_of_week].append({
                'start_time': wh.start_time.strftime('%H:%M'),
                'end_time': wh.end_time.strftime('%H:%M'),
                'slot_duration': wh.slot_duration,
            })

    weekly_data = []
    for day_code, day_name in barbers_models.WorkingHoursModel.DAYS_OF_WEEK:
        shifts = hours_by_day[day_code]
        is_closed = day_code in closed_days

        if not shifts and not is_closed:
            shifts = [{'start_time': '09:00', 'end_time': '18:00', 'slot_duration': 30}]

        weekly_data.append({
            'day_code': day_code,
            'day_name': day_name,
            'is_closed': is_closed,
            'shifts': shifts,
        })

    return weekly_data
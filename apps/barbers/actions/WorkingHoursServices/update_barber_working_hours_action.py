from typing import Dict, Any
from datetime import datetime
from barbers import models as barbers_models
from barbers import services as barbers_services


def UpdateBarberWorkingHoursAction(barber: barbers_models.BarberModel, post_data: Dict[str, Any]) -> None:
    """
    پردازش فرم و استخراج لیست شیفت‌های ارسالی برای هر روز هفته
    """
    for day_code, _ in barbers_models.WorkingHoursModel.DAYS_OF_WEEK:
        is_closed = f'is_closed_{day_code}' in post_data

        start_times = post_data.getlist(f'start_time_{day_code}[]') if hasattr(post_data, 'getlist') else post_data.get(f'start_time_{day_code}[]', [])
        end_times = post_data.getlist(f'end_time_{day_code}[]') if hasattr(post_data, 'getlist') else post_data.get(f'end_time_{day_code}[]', [])

        if isinstance(start_times, str):
            start_times = [start_times]
        if isinstance(end_times, str):
            end_times = [end_times]

        shifts = []
        if not is_closed:
            for st, et in zip(start_times, end_times):
                if st and et:
                    shifts.append({
                        'start_time': datetime.strptime(st, '%H:%M').time(),
                        'end_time': datetime.strptime(et, '%H:%M').time(),
                        'slot_duration': 30,
                    })

        barbers_services.SetBarberWorkingHoursService(
            barber=barber,
            day_of_week=day_code,
            shifts=shifts,
            is_closed=is_closed,
        )
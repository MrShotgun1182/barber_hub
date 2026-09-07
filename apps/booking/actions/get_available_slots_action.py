from datetime import datetime
from booking import services


def GetAvailableSlotsAction(
    barber_id: int, barber_service_ids: list[int], date_str: str
) -> dict:
    """
    اعتبارسنجی پارامترها و فراخوانی سرویس محاسبه سانس‌ها
    """
    if not barber_id or not barber_service_ids:
        return {
            'status': 'error',
            'message': 'شناسه آرایشگر یا خدمات ارسال نشده است.',
            'slots': [],
        }

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return {
            'status': 'error',
            'message': 'فرمت تاریخ نامعتبر است (فرمت صحیح: YYYY-MM-DD)',
            'slots': [],
        }

    slots = services.CalculateAvailableSlotsService(
        barber_id=barber_id,
        barber_service_ids=barber_service_ids,
        target_date=target_date,
    )

    return {
        'status': 'success',
        'date': date_str,
        'count': len(slots),
        'slots': slots,
    }
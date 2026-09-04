from typing import Any, Dict

from booking import services as booking_services


def UpdateAppointmentStatusAction(
    user: Any,
    appointment_id: int,
    new_status: str,
) -> Dict[str, Any]:
    """
    ارکستراسیون بروزرسانی وضعیت نوبت و بررسی دسترسی‌ها از طریق لایه سرویس
    """
    return booking_services.UpdateAppointmentStatusService(
        user=user,
        appointment_id=appointment_id,
        status=new_status,
    )
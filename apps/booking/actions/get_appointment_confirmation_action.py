from booking import services as booking_services


def GetAppointmentConfirmationAction(appointment_id: int, user) -> dict:
    """
    اکشن دریافت اطلاعات نوبت برای نمایش صفحه تاییدیه (فقط برای صاحب نوبت)
    """
    appointment = booking_services.GetAppointmentService(appointment_id)

    if appointment is None or appointment.customer.user_id != user.id:
        return {
            'status': 'error',
            'message': 'نوبت مورد نظر یافت نشد.',
            'appointment': None,
        }

    return {
        'status': 'success',
        'appointment': appointment,
    }
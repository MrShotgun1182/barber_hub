from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from booking.actions.get_appointment_confirmation_action import (
    GetAppointmentConfirmationAction,
)


@login_required
def BookingConfirmationView(request, appointment_id: int):
    """
    ویوی نمایش صفحه تاییدیه رزرو پس از ثبت موفق نوبت
    """
    result = GetAppointmentConfirmationAction(appointment_id, request.user)

    if result['status'] != 'success':
        return redirect('booking:select-barber')

    return render(
        request,
        'booking/booking_confirmation.html',
        {'appointment': result['appointment']},
    )
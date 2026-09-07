from booking import services as booking_services


def SubmitBookingAction(user, request_body: dict) -> dict:
    """
    اکشن ثبت اتمیک نوبت رزرو و بررسی تداخل زمان
    """
    try:
        barber_id = int(request_body.get('barber_id'))
        service_ids = request_body.get('barber_service_ids', [])
        booking_date = request_body.get('booking_date')
        start_time = request_body.get('start_time')
        end_time = request_body.get('end_time')

        appointment = booking_services.CreateAppointmentService(
            user=user,
            barber_id=barber_id,
            barber_service_ids=service_ids,
            booking_date=booking_date,
            start_time_str=start_time,
            end_time_str=end_time,
        )

        return {
            'status': 'success',
            'message': 'نوبت شما با موفقیت ثبت شد.',
            'appointment_id': appointment.id,
        }
    except ValueError as ve:
        return {
            'status': 'error',
            'message': str(ve),
        }
    except Exception:
        return {
            'status': 'error',
            'message': 'خطایی در ثبت نوبت رخ داد. مجدداً تلاش کنید.',
        }
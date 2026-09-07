import json
from appointments.services.create_appointment_service import (
    CreateAppointmentService,
)
from barbers.models.barber_model import BarberModel
from barbers.models.barber_service_model import BarberServiceModel


def GetBookingSummaryAction(
    barber_id: int, barber_service_ids: list[int]
) -> dict:
    """
    استخراج جزئیات فاکتور بر اساس IDهای ذخیره‌شده در sessionStorage
    """
    try:
        barber = BarberModel.objects.select_related('user').get(
            id=barber_id, is_active=True
        )
        services = BarberServiceModel.objects.filter(
            id__in=barber_service_ids, barber=barber, is_active=True
        ).select_related('service')

        services_data = []
        total_price = 0
        total_duration = 0

        for s in services:
            price = (
                s.custom_price
                if s.custom_price is not None
                else s.service.base_price
            )
            duration = (
                s.custom_duration_minutes
                if s.custom_duration_minutes is not None
                else s.service.default_duration_minutes
            )
            total_price += price
            total_duration += duration

            services_data.append({
                'name': s.service.name,
                'price': price,
                'duration': duration,
            })

        return {
            'status': 'success',
            'barber_name': barber.user.get_full_name() or barber.user.username,
            'services': services_data,
            'total_price': total_price,
            'total_duration': total_duration,
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def SubmitBookingAction(user, request_body: dict) -> dict:
    """
    اکشن ثبت نهایی رزرو
    """
    try:
        barber_id = int(request_body.get('barber_id'))
        service_ids = request_body.get('barber_service_ids', [])
        booking_date = request_body.get('booking_date')
        start_time = request_body.get('start_time')
        end_time = request_body.get('end_time')

        appointment = CreateAppointmentService(
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
        return {'status': 'error', 'message': str(ve)}
    except Exception as e:
        return {
            'status': 'error',
            'message': 'خطایی در ثبت نوبت رخ داد. مجدداً تلاش کنید.',
        }
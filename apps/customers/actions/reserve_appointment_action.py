from datetime import date, time
from django.db import transaction

from barbers import models as barbers_models
from booking import models as booking_models, services as booking_services
from customers import models as customers_models
from salon_services import models as salon_services_models


def ReserveAppointmentAction(
    customer: customers_models.CustomerModel,
    barber: barbers_models.BarberModel,
    service: salon_services_models.ServiceModel,
    appointment_date: date,
    start_time: time,
    end_time: time,
    price: int,
) -> booking_models.AppointmentModel:
    """
    ثبت و رزرو نوبت جدید برای مشتری در یک تراکنش اتمیک
    """
    with transaction.atomic():
        appointment = booking_services.CreateAppointmentService(
            customer=customer,
            barber=barber,
            service=service,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            price=price,
            status='PENDING',
        )
        return appointment  
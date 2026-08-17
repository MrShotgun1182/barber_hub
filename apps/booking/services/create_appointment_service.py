from datetime import date, time
from booking import models as booking_models
from barbers import models as barbers_models
from customers import models as customers_models
from salon_services import models as salon_services_models


def CreateAppointmentService(
    customer: customers_models.CustomerModel,
    barber: barbers_models.BarberModel,
    service: salon_services_models.ServiceModel,
    appointment_date: date,
    start_time: time,
    end_time: time,
    price: int,
    status: str = 'PENDING',
) -> booking_models.AppointmentModel:
    """
    ثبت نوبت جدید برای مشتری
    """
    return booking_models.AppointmentModel.objects.create(
        customer=customer,
        barber=barber,
        service=service,
        date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        price=price,
        status=status,
    )
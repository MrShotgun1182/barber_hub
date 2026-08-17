from typing import Optional
from django.db.models import QuerySet
from booking import models as booking_models
from customers import models as customers_models


def GetCustomerAppointmentsService(
    customer: customers_models.CustomerModel,
    status: Optional[str] = None,
) -> QuerySet[booking_models.AppointmentModel]:
    """
    دریافت لیست نوبت‌های یک مشتری با امکان فیلتر وضعیت
    """
    queryset = booking_models.AppointmentModel.objects.filter(customer=customer)
    if status is not None:
        queryset = queryset.filter(status=status)
    return queryset
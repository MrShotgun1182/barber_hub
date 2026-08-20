from django.db import transaction

from salon_services import services as salon_services_services


def DeleteSalonServiceAction(
    service_id: int,
) -> bool:
    """
    حذف خدمت سالن با شناسه خدمت در یک تراکنش اتمیک
    """
    with transaction.atomic():
        return salon_services_services.DeleteServiceService(
            service_id=service_id,
        )
from django.db import transaction

from salon_services import (
    models as salon_services_models,
    services as salon_services_services,
)


def ToggleServiceStatusAction(
    service: salon_services_models.ServiceModel,
) -> salon_services_models.ServiceModel:
    """
    تغییر وضعیت فعال/غیرفعال بودن ارائه خدمت سالن در یک تراکنش اتمیک
    """
    with transaction.atomic():
        updated_service = salon_services_services.UpdateServiceService(
            service=service,
            is_active=not service.is_active,
        )
        return updated_service
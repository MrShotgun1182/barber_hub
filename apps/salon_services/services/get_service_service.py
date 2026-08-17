from typing import Optional
from salon_services import models


def GetServiceService(service_id: int) -> Optional[models.ServiceModel]:
    """
    دریافت اطلاعات یک خدمت بر اساس شناسه
    """
    try:
        return models.ServiceModel.objects.get(id=service_id)
    except models.ServiceModel.DoesNotExist:
        return None
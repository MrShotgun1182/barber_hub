from booking import services as booking_services


def GetBookingSummaryAction(
    barber_id: int, barber_service_ids: list[int]
) -> dict:
    """
    اکشن دریافت خلاصه اطلاعات فاکتور رزرو
    """
    try:
        summary_data = booking_services.GetBookingSummaryService(
            barber_id=barber_id,
            barber_service_ids=barber_service_ids,
        )
        return {
            'status': 'success',
            **summary_data,
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
        }
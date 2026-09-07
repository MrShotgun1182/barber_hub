import json
from django.http import JsonResponse
from django.shortcuts import render
from booking import actions as booking_actions


def SelectDatetimeView(request):
    """
    ویوی گام سوم: انتخاب تاریخ و دریافت سانس‌های آزاد
    """
    # اگر درخواست AJAX جهت دریافت سانس‌های یک روز خاص باشد
    if (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.GET.get('format') == 'json'
    ):
        barber_id = request.GET.get('barber_id')
        service_ids_raw = request.GET.get('service_ids', '[]')
        date_str = request.GET.get('date')

        try:
            barber_id = int(barber_id)
            service_ids = (
                json.loads(service_ids_raw)
                if isinstance(service_ids_raw, str)
                else service_ids_raw
            )
        except (ValueError, TypeError):
            return JsonResponse(
                {'status': 'error', 'message': 'ورودی‌ها نامعتبر هستند.'},
                status=400,
            )

        result = booking_actions.GetAvailableSlotsAction(
            barber_id=barber_id,
            barber_service_ids=service_ids,
            date_str=date_str,
        )
        return JsonResponse(result)

    return render(request, 'appointments/select_datetime.html')
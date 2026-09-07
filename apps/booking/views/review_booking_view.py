import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from booking.actions.get_booking_summary_action import GetBookingSummaryAction
from booking.actions.submit_booking_action import SubmitBookingAction


@login_required
def ReviewBookingView(request):
    """
    ویوی مدیریت پیش‌نمایش فاکتور و ثبت نهایی نوبت
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = SubmitBookingAction(request.user, data)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'فرمت داده ارسال‌شده اشتباه است.'},
                status=400,
            )

    if request.GET.get('action') == 'get_summary':
        barber_id = request.GET.get('barber_id')
        service_ids_raw = request.GET.get('service_ids', '[]')
        try:
            barber_id = int(barber_id)
            service_ids = json.loads(service_ids_raw)
            summary = GetBookingSummaryAction(barber_id, service_ids)
            return JsonResponse(summary)
        except Exception:
            return JsonResponse(
                {'status': 'error', 'message': 'ورودی‌ها نامعتبر هستند.'},
                status=400,
            )

    return render(request, 'booking/review_booking.html')
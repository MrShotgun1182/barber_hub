import json
from django.http import JsonResponse
from django.shortcuts import render
from barbers import actions


def SelectBarberAndServiceView(request):
    """
    ویوی انتخاب آرایشگر و خدمت
    """
    options_data = actions.GetBookingOptionsAction()

    # اگر درخواست AJAX/Fetch باشه، مستقیم پاسخ JSON میده
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse(options_data)

    # در غیر این صورت، تمپلیت HTML رو به همراه ساختار JSON رندر می‌کنه
    context = {
        'barbers_json': json.dumps(options_data['barbers'], ensure_ascii=False)
    }
    return render(request, 'booking/select_barber_and_service.html', context)
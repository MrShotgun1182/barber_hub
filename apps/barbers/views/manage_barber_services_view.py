from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from barbers import actions as barbers_actions

@login_required
def ManageBarberServicesView(request):
    """
    مدیریت نمایش و ثبت خدمات اختصاصی آرایشگر
    """
    barber = getattr(request.user, 'barber_profile', None)
    if not barber:
        return redirect('barbers:login')

    success_message = None

    if request.method == 'POST':
        barbers_actions.UpdateBarberServicesAction(barber, request.POST)
        success_message = "تنظیمات خدمات با موفقیت به‌روزرسانی شد."

    services_data = barbers_actions.GetBarberServicesDataAction(barber)

    context = {
        'services_data': services_data,
        'success_message': success_message,
    }

    return render(request, 'barbers/salon_services/manage_services.html', context)
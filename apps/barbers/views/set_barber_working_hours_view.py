from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from barbers import actions as barbers_actions


@login_required
def SetBarberWorkingHoursView(request):
    """
    نمایش و به‌روزرسانی ساعات کاری هفتگی آرایشگر
    """
    barber = getattr(request.user, 'barber_profile', None)
    if not barber:
        return redirect('barbers:barbers_dashboard')

    success_message = None

    if request.method == 'POST':
        barbers_actions.UpdateBarberWorkingHoursAction(barber, request.POST)
        success_message = "ساعات کاری با موفقیت به‌روزرسانی شد."

    weekly_data = barbers_actions.GetBarberWorkingHoursDataAction(barber)

    context = {
        'weekly_data': weekly_data,
        'success_message': success_message,
    }

    return render(request, 'barbers/WorkingHoursServices/manage_working_hours.html', context)
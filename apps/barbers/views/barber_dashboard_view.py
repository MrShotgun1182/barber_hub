from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from barbers import actions as barbers_actions


@login_required
def BarberDashboardView(request):
    """
    نمایش داشبورد آرایشگر با دریافت اطلاعات نوبت‌های واقعی امروز
    """
    result = barbers_actions.GetBarberTodayAppointmentsAction(user=request.user)

    context = {
        'dashboard': {
            'today_appointments': result.get('appointments', []),
            'today_appointments_count': result.get('count', 0),
            'error': result.get('error'),
        }
    }

    return render(request, 'barbers/dashboard.html', context)
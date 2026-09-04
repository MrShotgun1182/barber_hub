from django.shortcuts import render, redirect
from admin_panel import Actions as admin_actions


def DashboardView(request):
    """
    نمایش داشبورد مدیریت شامل لیست نوبت‌های امروز تمامی مشتریان
    """
    if not request.user.is_authenticated or not (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    ):
        return redirect('admin_login')

    dashboard_data = admin_actions.GetTodayAppointmentsAction()

    context = {
        'dashboard': dashboard_data,
    }

    return render(request, 'admin_panel/dashboard.html', context)
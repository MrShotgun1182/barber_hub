from django.shortcuts import render, redirect
from admin_panel import Actions as admin_actions


def SalonServicesListView(request):
    """
    نمایش لیست کامل خدمات سالن جهت مدیریت در پنل ادمین
    """
    if not request.user.is_authenticated or not (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    ):
        return redirect('admin_panel:admin_login')

    data = admin_actions.GetAllSalonServicesAction()

    context = {
        'services': data['services'],
    }

    return render(request, 'admin_panel/salon_service/salon_services_list.html', context)
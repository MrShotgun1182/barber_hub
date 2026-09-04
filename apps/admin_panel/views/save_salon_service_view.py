from django.shortcuts import render, redirect
from salon_services import services as salon_services_services
from admin_panel import Actions as admin_actions


def SaveSalonServiceView(request, service_id: int = None):
    """
    مدیریت فرم ایجاد و ویرایش خدمت سالن
    """
    if not request.user.is_authenticated or not (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    ):
        return redirect('admin_panel:admin_login')

    service = None
    if service_id:
        service = salon_services_services.GetServiceService(service_id)
        if not service:
            return redirect('admin_panel:salon_services_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        base_price = int(request.POST.get('base_price', 0))
        default_duration_minutes = int(
            request.POST.get('default_duration_minutes', 45)
        )
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'

        if service:
            admin_actions.UpdateSalonServiceAction(
                service=service,
                name=name,
                base_price=base_price,
                default_duration_minutes=default_duration_minutes,
                description=description,
                is_active=is_active,
            )
        else:
            admin_actions.CreateSalonServiceAction(
                name=name,
                base_price=base_price,
                default_duration_minutes=default_duration_minutes,
                description=description,
                is_active=is_active,
            )

        return redirect('admin_panel:salon_services_list')

    context = {
        'service': service,
    }
    return render(request, 'admin_panel/salon_service/save_salon_service.html', context)
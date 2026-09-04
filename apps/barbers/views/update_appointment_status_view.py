from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from barbers import actions as barbers_actions


@login_required
@require_POST
def UpdateAppointmentStatusView(request, appointment_id: int):
    """
    دریافت درخواست POST برای تغییر وضعیت نوبت و ارجاع به اکشن
    """
    status = request.POST.get('status')
    if status:
        barbers_actions.UpdateAppointmentStatusAction(
            user=request.user,
            appointment_id=appointment_id,
            new_status=status,
        )

    return redirect('barbers:barbers_dashboard')
from django.shortcuts import render, redirect
from admin_panel import Actions as admin_actions


def AdminLoginView(request):
    """
    مدیریت درخواست و پردازش ورود مدیر به داشبورد
    """
    if request.user.is_authenticated and (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    ):
        return redirect('admin_panel:admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        result = admin_actions.AdminLoginAction(request, username=username, password=password)

        if result['success']:
            return redirect('admin_panel:admin_dashboard')

        return render(
            request,
            'accounts/admin_login.html',
            {'error': result['error']},
        )

    return render(request, 'admin_panel/login.html')
from django.shortcuts import render, redirect
from barbers import forms as barbers_forms
from barbers import actions as barbers_actions


def BarberLoginView(request):
    """
    مدیریت فرم ورود آرایشگر و ارجاع کامل منطق ورود به لایه اکشن
    """
    if request.method == 'POST':
        form = barbers_forms.BarberLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            result = barbers_actions.BarberLoginAction(
                request, username=username, password=password
            )

            if result['success']:
                return redirect('barbers:barbers_dashboard')

            form.add_error(None, result['error'])
    else:
        form = barbers_forms.BarberLoginForm()

    return render(request, 'barbers/login.html', {'form': form})
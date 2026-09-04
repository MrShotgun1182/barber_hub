from barbers import views
from django.urls import path

app_name = 'barbers'

urlpatterns = [
    path('login/', views.BarberLoginView, name='barbers_login'),
    path('dashboard/', views.BarberDashboardView, name='barbers_dashboard'),
    path('appointments/<int:appointment_id>/status/',views.UpdateAppointmentStatusView,name='update_appointment_status'),
    
]
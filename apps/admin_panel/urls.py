from admin_panel import views
from django.urls import path

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.DashboardView, name='admin_dashboard'),
    path('login/', views.AdminLoginView, name='admin_login'),
    path('services/', views.SalonServicesListView, name='salon_services_list'),
    path('services/create/', views.SaveSalonServiceView, name='create_salon_service'),
    path('services/<int:service_id>/edit/', views.SaveSalonServiceView,name='edit_salon_service'),
]
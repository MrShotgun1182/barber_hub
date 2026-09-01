from admin_panel import views
from django.urls import path

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.DashboardView, name='dashboard'),
]
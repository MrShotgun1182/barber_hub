from django.urls import path
from booking import views

app_name = 'otp'

urlpatterns = [
    path('otp/', views.OTPPageView, name='otp_page'),
    path('api/send/', views.SendOTPView, name='send_otp'),
    path('api/verify/', views.VerifyOTPView, name='verify_otp'),
]
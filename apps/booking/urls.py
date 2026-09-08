from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('otp/', views.OTPPageView, name='otp_page'),
    path('api/send/', views.SendOTPView, name='send_otp'),
    path('api/verify/', views.VerifyOTPView, name='verify_otp'),
    path('select-barber/', views.SelectBarberServiceView, name='select-barber'),
    path('select-datetime/', views.SelectDatetimeView, name='select-datetime'),
    path('review/', views.ReviewBookingView, name='review'),
]
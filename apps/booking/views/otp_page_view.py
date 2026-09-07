from django.shortcuts import render

def OTPPageView(request):
    """ویوی رندر کردن صفحه اختصاصی گام اول (OTP)"""
    return render(request, 'booking/otp.html')
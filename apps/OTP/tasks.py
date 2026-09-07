from celery import shared_task
from OTP import services as OTP_services

@shared_task
def SendOTPSMSTask(phone_number: str, code: str):
    """تاسک سلری برای ارسال غیرهمزمان پیامک"""
    text = f"کد تایید شما در باربر هاب: {code}\nاعتبار: ۲ دقیقه"
    return OTP_services.SendSMSService(phone_number, text)
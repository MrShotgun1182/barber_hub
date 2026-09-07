from OTP import models, services, tasks

def SendOTPAction(phone_number: str) -> dict:
    """اکشن مدیریت فرآیند درخواست و ارسال کد OTP"""
    # ۱. تولید کد
    code = services.GenerateOTPCodeService(length=5)
    
    # ۲. ثبت در دیتابیس
    models.OTPModel.objects.create(
        phone_number=phone_number,
        code=code
    )
    
    # ۳. ارسال غیرهمزمان با Celery
    tasks.SendOTPSMSTask.delay(phone_number, code)
    
    return {
        'status': 'success',
        'message': 'کد تایید با موفقیت ارسال شد'
    }
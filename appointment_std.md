# سند فنی جامع پیاده‌سازی سیستم رزرو نوبت (Barber Hub)

---

## ۱. ساختار لایه‌ای و چرخه جریان داده (Data Flow Architecture)

### ۱.۱. جریان ۵ مرحله‌ای فرآیند رزرو

1. **مرحله ۱ (انتخاب خدمت و آرایشگر):** انتخاب خدمت پایه و آرایشگر ارائه‌دهنده توسط مشتری.
2. **مرحله ۲ (محاسبه و انتخاب زمان):** ارسال درخواست AJAX جهت محاسبه پویا و دریافت اسلات‌های زمانی آزاد و انتخاب اسلات توسط مشتری.
3. **مرحله ۳ (ذخیره‌سازی موقت در فرانت‌اند):** ذخیره پیش‌نویس انتخاب‌ها در `sessionStorage` مرورگر جهت جلوگیری از ثبت داده‌های ناقص یا یتیم (Orphan Data) در دیتابیس.
4. **مرحله ۴ (احراز هویت پیامکی):** دریافت نام و شماره موبایل، ارسال و اعتبارسنجی کد یک‌بارمصرف OTP.
5. **مرحله ۵ (ثبت نهایی در بک‌اند):** ارسال داده‌های موجود در `sessionStorage` همراه با نشست کاربر به اکشن `BookAppointmentAction` و ایجاد رکورد نوبت در دیتابیس.

### ۱.۲. ساختار کلید پیش‌نویس در `sessionStorage`

```json
{
  "booking_draft": {
    "barber_id": 1,
    "service_id": 3,
    "date": "2026-09-10",
    "start_time": "11:45",
    "end_time": "12:30"
  }
}

```

---

## ۲. اپلیکیشن احراز هویت پیامکی (`apps/otp`)

### ۲.۱. مدل دیتابیس (`apps/otp/models/otp_model.py`)

* **فیلدها:**
* `phone_number`: شماره موبایل دریافت‌کننده (CharField).
* `code`: کد ۵ رقمی تولیدشده (CharField).
* `is_used`: وضعیت استفاده از کد (BooleanField).
* `created_at`: زمان ایجاد (DateTimeField).
* `expires_at`: زمان انقضا (DateTimeField - اعتبار ۲ دقیقه‌ای).



### ۲.۲. لایه سرویس (`apps/otp/services/`)

* **`send_otp_service.py` (`SendOtpService`):** تولید کد ۵ رقمی، ذخیره در دیتابیس (`OTPModel`) و ارسال پیامک از طریق پنل پیامکی.
* **`verify_otp_service.py` (`VerifyOtpService`):** اعتبارسنجی کد ورودی، بررسی عدم انقضا و علامت‌گذاری به عنوان `is_used=True`.

---

## ۳. لایه سرویس‌های رزرو نوبت (`apps/appointments/services/`)

### ۳.۱. سرویس محاسبه اسلات‌های زمانی آزاد (`get_available_slots_service.py`)

* **منطق محاسباتی:**
1. نگاشت تاریخ انتخابی به روز هفته (۰=شنبه تا ۶=جمعه).
2. دریافت ساعات کاری آرایشگر از `WorkingHoursModel` و مشخصات خدمت از `BarberServiceModel`.
3. تعیین گام زمانی (`slot_step_minutes`) و مدت زمان خدمت (`service_duration`).
4. اعمال قانون **امکان تکمیل نوبت تا ۳۰ دقیقه پس از پایان ساعت کاری** (`max_allowed_end = work_end_time + 30min`).
5. دریافت نوبت‌های فعال از `AppointmentModel` و فیلتر اسلات‌های دارای تداخل زمانی (`has_overlap`).



### ۳.۲. سرویس ثبت نوبت (`create_appointment_service.py`)

* درج مستقیم رکورد نوبت در دیتابیس (`AppointmentModel`) با ثبت قیمت قطعی، تاریخ و بازه زمانی مشخص.

---

## ۴. لایه اکشن‌ها (Action Layer)

### ۴.۱. اکشن احراز هویت و ثبت‌نام مشتری (`apps/accounts/actions/auth_phone_action.py`)

* فراخوانی `VerifyOtpService`.
* ایجاد یا دریافت کاربر در `UserModel` با نقش `CUSTOMER` و ساخت پروفایل مربوطه در `CustomerModel`.
* اجرای فرآیند ورود کاربر به نشست (`login(request, user)`).

### ۴.۲. اکشن ثبت رزرو نوبت (`apps/appointments/actions/book_appointment_action.py`)

* **ارکستراسیون فرآیند:**
1. اعتبارسنجی مجدد زمان انتخابی جهت جلوگیری از Race Condition (فراخوانی سرویس محاسبه اسلات‌ها).
2. استخراج قیمت پایه یا اختصاصی خدمت.
3. فراخوانی `CreateAppointmentService` جهت درج نوبت.



---

## ۵. لایه ویوها و تمپلیت‌ها (Views & Templates)

* **`get_available_slots_view.py` (`GetAvailableSlotsView`):** اندپوینت API/AJAX جهت بازگرداندن اسلات‌های آزاد بر اساس `barber_id`, `service_id` و `date`.
* **`send_otp_view.py` / `verify_otp_view.py`:** ویوهای ارسال و تایید کد OTP.
* **`book_appointment_view.py` (`BookAppointmentView`):** دریافت درخواست ثبت رزرو، ارسال داده‌ها به `BookAppointmentAction` و هدایت کاربر به صفحه تایید نهایی.

---

آیا این داکیومنت فنی مورد تایید شما هست تا وارد مرحله اجرای گام‌به‌گام کدهای پروژه بشویم؟
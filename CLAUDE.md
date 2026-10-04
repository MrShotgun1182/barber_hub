# CLAUDE.md — قوانین و راهنمای پروژه Barber Hub

این فایل مرجع قوانین، معماری و قراردادهای پروژه است. قبل از هر تغییری در کد، این فایل را بخوان.

---

## ۱. معرفی پروژه

**Barber Hub** یک سامانه رزرو نوبت آرایشگاه به زبان فارسی است:
- مشتری با شماره موبایل و کد OTP وارد می‌شود، آرایشگر و خدمت را انتخاب می‌کند و نوبت رزرو می‌کند.
- آرایشگر پنل اختصاصی (نوبت‌های امروز، خدمات، ساعات کاری) دارد.
- مدیر (MANAGER) پنل مدیریت (خدمات پایه سالن، نوبت‌های امروز) دارد.

زبان پروژه فارسی است: تمام `verbose_name`ها، docstringها، پیام‌های خطا و کامنت‌ها باید فارسی باشند.

---

## ۲. پشته فناوری (Tech Stack)

| بخش | فناوری |
| --- | --- |
| بک‌اند | Django `>=5.0,<6.0` (ولیدیشن رمز غیرفعال است) |
| دیتابیس | PostgreSQL 15 |
| تسک غیرهمزمان | Celery + Redis |
| پیامک | پکیج `melipayamak` |
| فرانت‌اند | Tailwind CSS v4 (بدون فایل کانفیگ، تم داخل `input.css`) |
| کانتینر | Docker + docker-compose |

---

## ۳. دستورات کلیدی

```bash
# اجرای کل استک (وب + دیتابیس + redis + celery)
docker compose up --build

# ساخت و اجرای مایگریشن‌ها
python manage.py makemigrations
python manage.py migrate

# اجرای سرور توسعه
python manage.py runserver

# اجرای Celery worker (برای ارسال پیامک OTP)
celery -A core worker --loglevel=info

# فرانت‌اند: کامپایل Tailwind
cd frontend
npm run dev     # حالت watch → خروجی frontend/static/dist/output.css
npm run build   # حالت minify برای پروداکشن

# تست‌ها
python manage.py test
```

> **نکته:** فایل CSS نهایی در `frontend/static/dist/output.css` ساخته می‌شود و در تمپلیت‌ها با `{% static 'dist/output.css' %}` لود می‌شود. پس از افزودن کلاس‌های جدید Tailwind، باید کامپایلر در حال اجرا باشد.

---

## ۴. معماری لایه‌ای (قانون طلایی)

جریان داده **یک‌طرفه** است و هیچ لایه‌ای نباید لایه بالاتر را صدا بزند:

```
Request → View → Action → Service → Model/DB
```

| لایه | مسئولیت | مجاز به |
| --- | --- | --- |
| **View** | دریافت request، پارس ورودی، رندر تمپلیت یا JsonResponse | فقط فراخوانی Action |
| **Action** | ارکستراسیون سرویس‌ها، اعتبارسنجی، مدیریت خطا، `transaction.atomic` | فراخوانی Service |
| **Service** | منطق خالص دیتابیس و محاسبات | کار با Model/ORM |
| **Model** | تعریف ساختار دیتابیس | — |

**قوانین سخت:**
- ویو **نباید** مستقیم سرویس را صدا بزند؛ فقط Action.
- ویو **نباید** مستقیم کوئری ORM بزند.
- منطق کسب‌وکار در Action و Service است، نه در View و نه در Model.
- Action برای عملیات چندگانه/اتمیک، `transaction.atomic()` را در خودش یا در سرویس صداکننده می‌پیچد.

**شکل خروجی اکشن‌ها:** اکشن‌ها معمولاً یک `dict` برمی‌گردانند و خطاها را درون خودشان catch می‌کنند تا به ویو نشت نکند:

```python
# الگوی متداول اکشن
def SomeAction(...) -> dict:
    try:
        data = some_services.SomeService(...)
        return {'status': 'success', 'message': '...', **data}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطایی رخ داد. مجدداً تلاش کنید.'}
```

> برخی اکشن‌های ورود، از کلید `success` (بولین) و `error` استفاده می‌کنند (مثل `BarberLoginAction`). الگوی غالب در پاسخ‌های API کلیدهای `status`/`message` است. هنگام افزودن اکشن جدید، به قرارداد اکشن‌های هم‌خانواده‌اش نگاه کن.

---

## ۵. قواعد نام‌گذاری

### نام فایل‌ها — snake_case با پسوند لایه

| لایه | الگوی فایل | الگوی نام تابع/کلاس |
| --- | --- | --- |
| Models | `[name]_model.py` | `[Name]Model` |
| Services | `[action]_[name]_service.py` | `[Action][Name]Service` |
| Actions | `[operation]_[name]_action.py` | `[Operation][Name]Action` |
| Views | `[name]_view.py` | `[Name]View` |
| Templates | `[name].html` | — |

**مثال‌ها:**
- `apps/booking/services/create_appointment_service.py` → تابع `CreateAppointmentService`
- `apps/booking/actions/submit_booking_action.py` → تابع `SubmitBookingAction`
- `apps/booking/views/select_datetime_view.py` → تابع `SelectDatetimeView`

### نکات مهم
- توابع در ویو/اکشن/سرویس **PascalCase** هستند (نه snake_case)، حتی در ویوها. ویوها **تابع** هستند نه کلاس (استثنا: `django.views.generic.TemplateView` که فقط در `core/urls.py` استفاده شده).
- **همه** فایل‌های `views/`، `actions/`، `services/`، `models/` یک `__init__.py` دارند که نمادها را re-export می‌کند. بعد از افزودن فایل جدید، حتماً آن را در `__init__.py` همان پوشه import کن.
- در `admin_panel` پوشه اکشن‌ها با حرف بزرگ است: `Actions/` (ناسازگاری تاریخی). در بقیه اپ‌ها `actions/` است. الگوی همان اپ را رعایت کن.

### الگوی import
پوشه `apps/` به `sys.path` اضافه شده (در `core/settings.py`). پس اپ‌ها با **نام خالی** import می‌شوند، نه با پیشوند `apps.`:

```python
from booking import services as booking_services
from barbers import models as barbers_models
from accounts import services as accounts_services
```

الگوی `import ... as ..._models` / `..._services` رایج است تا از تداخل نام جلوگیری شود. همین سبک را ادامه بده.

---

## ۶. ساختار پروژه

```
barber_hub/
├── core/                      # تنظیمات ریشه: settings.py, urls.py, celery.py
├── apps/                      # همه اپ‌ها (روی sys.path)
│   ├── accounts/              # UserModel (AbstractUser + phone_number + role)
│   ├── barbers/               # BarberModel, BarberServiceModel, WorkingHoursModel
│   ├── customers/             # CustomerModel, CustomerHairstyleModel
│   ├── admin_panel/           # AdminPanelModel (پروفایل مدیر) + پوشه Actions/ (بزرگ)
│   ├── booking/               # AppointmentModel + فلوی ویزارد رزرو
│   ├── salon_services/        # ServiceModel (خدمات پایه سالن)
│   └── OTP/                   # OTPModel + Celery task ارسال پیامک
├── frontend/                  # Tailwind + تمپلیت‌های سراسری + استاتیک
│   ├── static/src/input.css   # تم و رنگ‌های سفارشی (cream/sage)
│   ├── static/dist/output.css # خروجی کامپایل‌شده Tailwind
│   └── templates/core/        # base.html, barber_base.html, admin_base.html, landing.html
└── manage.py
```

هر اپ داخل `apps/` ساختار زیر را دارد:
`models/`, `views/`, `actions/`, `services/`, `templates/<app>/`, `migrations/`, `admin.py`, `urls.py` (اختیاری).

> **اپ‌های بدون `urls.py`:** `OTP`, `customers`, `salon_services`. این‌ها از طریق ویوهای اپ‌های دیگر (مثل `booking`) یا به‌صورت داخلی استفاده می‌شوند. در `core/urls.py` ثبت نمی‌شوند.

---

## ۷. مدل‌های دامنه و روابط کلیدی

- **`accounts.UserModel`** (سفارشی، `AUTH_USER_MODEL`): `AbstractUser` + `phone_number` (unique, ۱۱ رقم) + `role` در `{CUSTOMER, BARBER, MANAGER}`.
- **`barbers.BarberModel`**: `OneToOne` به User با `related_name='barber_profile'`.
- **`customers.CustomerModel`**: `OneToOne` به User با `related_name='customer_profile'`.
- **`admin_panel.AdminPanelModel`**: `OneToOne` به User با `related_name='manager_profile'`.
- **`salon_services.ServiceModel`**: خدمت پایه با `base_price` و `default_duration_minutes`.
- **`barbers.BarberServiceModel`**: خدمت اختصاصی آرایشگر (`unique_together=(barber, service)`) با `custom_price` و `custom_duration_minutes` که اگر `null` باشند، مقادیر پایه `ServiceModel` اعمال می‌شوند.
- **`barbers.WorkingHoursModel`**: ساعات کاری هفتگی؛ `day_of_week` از **۰=شنبه تا ۶=جمعه** (نگاشت پایتون: `(date.weekday() + 2) % 7`).
- **`booking.AppointmentModel`**: نوبت با `ManyToMany` به `BarberServiceModel`، `total_price`/`total_duration_minutes` ذخیره‌شده، و `status` در `{PENDING, CONFIRMED, COMPLETED, CANCELLED}`.

### اعتبارسنجی زمان
در همه‌جا از فرمول استاندارد تداخل استفاده کن:
`max(start1, start2) < min(end1, end2)` → تداخل دارد.
فقط نوبت‌های با وضعیت `PENDING` و `CONFIRMED` در بررسی آزاد بودن اسلات لحاظ می‌شوند.

---

## ۸. فلوی رزرو (Wizard)

چهار گام مجزا، هر گام **ویو/اکشن/سرویس اختصاصی** دارد. State در `sessionStorage` مرورگر نگه داشته می‌شود:

1. **OTP** — `SendOTPView`/`VerifyOTPView` → `SendOTPAction`/`VerifyOTPAction`
2. **انتخاب آرایشگر و خدمت** — `SelectBarberAndServiceView` → `GetBookingOptionsAction`
3. **انتخاب تاریخ و سانس** — `SelectDatetimeView` → `GetAvailableSlotsAction` → `CalculateAvailableSlotsService`
4. **بازبینی و ثبت نهایی** — `ReviewBookingView` → `SubmitBookingAction` → `CreateAppointmentService`

مسیرها در `apps/booking/urls.py` با `app_name = 'booking'` و نام‌گذاری namespace دار.

جزئیات کامل فلو در `appointment_std.md` آمده است.

---

## ۹. OTP و پیامک

- کد ۶ رقمی با `secrets` تولید می‌شود (`GenerateOTPCodeService`)، در `OTPModel` ذخیره و **اعتبار ۲ دقیقه** دارد.
- ارسال پیامک **غیرهمزمان** با Celery است: `SendOTPSMSTask.delay(...)` → `SendSMSService` (پکیج `melipayamak`).
- اعتبارنامه‌های پیامک از `.env` خوانده می‌شوند: `MELIPAYAMAK_USERNAME`, `MELIPAYAMAK_PASSWORD`, `MELIPAYAMAK_FROM`.
- تأیید کد به‌صورت اتمیک `is_used=True` می‌کند تا استفاده مجدد ممکن نباشد.

---

## ۱۰. URLها

- `core/urls.py`: `admin/` (Django admin)، `accounts/`، `admin_panel/`، `barber/`، `booking/`، و `''` برای landing.
- اپ‌ها `app_name` تعریف می‌کنند و URLها با namespace صدا زده می‌شوند: `{% url 'barbers:barbers_dashboard' %}`.
- ویوها به‌صورت تابعی مستقیم ثبت می‌شوند: `path('...', views.SomeView, name='some_name')`.

---

## ۱۱. تمپلیت‌ها و فرانت‌اند

- تمپلیت‌های سراسری در `frontend/templates/core/` (`DIRS` در settings). تمپلیت‌های هر اپ در `apps/<app>/templates/<app>/`.
- ارث‌بری: از `core/base.html` (و برای پنل‌ها `core/barber_base.html` / `core/admin_base.html`).
- زبان پیش‌فرض `fa` و `dir="rtl"` است.
- Tailwind v4: **فایل `tailwind.config.js` وجود ندارد**. محتوا خودکار از تمپلیت‌ها اسکن می‌شود و تم سفارشی داخل `frontend/static/src/input.css` با `@theme` تعریف شده (پالت `cream-*` و `sage-*`).
- برای استفاده از رنگ‌های برند از کلاس‌هایی مثل `bg-sage-500`، `text-cream-100` استفاده کن.

---

## ۱۲. احراز هویت و دسترسی

- ورود مشتری: موبایل + OTP → `GetOrCreateUserByPhoneService` کاربر را با نقش `CUSTOMER` می‌سازد و `login()` می‌کند.
- ورود آرایشگر: فقط کاربران با `role == 'BARBER'` و پروفایل `is_active=True` (اکشن `BarberLoginAction`).
- ورود مدیر: `role == 'MANAGER'` یا `is_staff` یا `is_superuser` (اکشن `AdminLoginAction`).
- ویوهای پنل‌ها با `@login_required` و بررسی دستی نقش محافظت می‌شوند. هنگام افزودن ویو جدید، محافظت دسترسی را فراموش نکن.

---

## ۱۳. نکات و بدهی‌های فنی شناخته‌شده (Gotchas)

این موارد را هنگام کار روی کد در نظر بگیر؛ **بدون درخواست صریح آن‌ها را «درست» نکن**، فقط آگاه باش:

- `SECRET_KEY`، `DEBUG=True` و `AUTH_PASSWORD_VALIDATORS = []` در `settings.py` سخت‌کد شده‌اند (حالت توسعه). برای پروداکشن باید اصلاح شوند.
- در `apps/OTP/` هم پکیج `models/` و هم فایل `apps/OTP/models.py` وجود دارد. پکیج برنده می‌شود و `models.py` عملاً کد مرده است — تغییرات را در `models/OTP_model.py` بده.
- `apps/OTP/views.py` یک فایل است (نه پکیج `views/`) و `urls.py` ندارد؛ از طریق `booking` استفاده می‌شود.
- `SendSMSService` شامل `print()`های دیباگ است که مقادیر حساس را چاپ می‌کنند.
- پوشه `Actions/` (بزرگ) فقط در `admin_panel` — ناسازگار با بقیه اپ‌ها.
- درخواست‌های AJAX/Fetch برای دریافت JSON، هدر `x-requested-with: XMLHttpRequest` یا پارامتر `?format=json` را می‌فرستند (الگوی `SelectBarberAndServiceView`).

---

## ۱۴. چک‌لیست افزودن قابلیت جدید

1. مدل (در صورت نیاز) → `models/<name>_model.py` + ثبت در `models/__init__.py` + مایگریشن.
2. سرویس‌ها → `services/<action>_<name>_service.py` + ثبت در `services/__init__.py`.
3. اکشن → `actions/<operation>_<name>_action.py` + ثبت در `actions/__init__.py`.
4. ویو → `views/<name>_view.py` + ثبت در `views/__init__.py`.
5. مسیر → `urls.py` اپ با `name` مناسب.
6. تمپلیت (در صورت نیاز) → `templates/<app>/<name>.html`.
7. رعایت زبان فارسی در پیام‌ها و `verbose_name`ها.

---

## ۱۵. سبک کد

- docstring فارسی یک‌خطی برای هر تابع اصلی (نقش لایه را توضیح دهد).
- Type hint برای پارامترهای سرویس/اکشن (`barber_id: int`, `barber_service_ids: list[int]`, `-> dict`).
- کامنت‌های شماره‌دار فارسی (`# ۱. ...`, `# ۲. ...`) برای مراحل داخل توابع طولانی.
- نام متغیرها و توابع: انگلیسی. پیام‌ها/برچسب‌ها: فارسی.
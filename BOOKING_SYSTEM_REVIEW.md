# گزارش بررسی سیستم نوبت‌دهی — Barber Hub

**تاریخ بررسی:** ۱۴۰۵/۰۷/۱۲ (2026-10-04)
**دامنه بررسی:** کل فلوی رزرو نوبت (OTP → انتخاب آرایشگر/خدمت → انتخاب زمان → ثبت نهایی) به‌همراه ساعات کاری، وضعیت نوبت و پنل‌های مرتبط.
**روش:** مطالعه کامل لایه‌های View/Action/Service/Model/Template در اپ‌های `booking`, `barbers`, `customers`, `salon_services`, `OTP`, `admin_panel` و راستی‌آزمایی پارامترها و امضاهای بین‌لایه‌ای.

> این گزارش فقط **مشکلات** را مستند می‌کند. هیچ کدی تغییر داده نشده است.

---

## خلاصه اجرایی

| # | شدت | عنوان | فایل کلیدی |
| --- | --- | --- | --- |
| ۱ | 🔴 بحرانی | کرش محاسبه سانس در روزهای چندشیفتی (`.get()` روی چند رکورد) | `booking/services/calculate_available_slots_service.py:36` |
| ۲ | 🔴 بحرانی | عدم محدودیت تلاش برای OTP (امکان بروت‌فورس ۶ رقمی) | `OTP/services/verify_otp_service.py:5` |
| ۳ | 🟠 بالا | نام خدمت در داشبورد آرایشگر اشتباه است (`appointment.service`) | `barbers/templates/barbers/dashboard.html:53,104` |
| ۴ | 🟠 بالا | رقابت (Race Condition) در ثبت نوبت و دوباره‌رزروی | `booking/services/create_appointment_service.py:54` |
| ۵ | 🟠 بالا | دو اکشن قدیمی با امضای نامعتبر → خطای TypeError | `customers/actions/reserve_appointment_action.py:23` |
| ۶ | 🟠 بالا | نبود `LOGIN_URL` → ریدایرکت `login_required` به مسیر ۴۰۴ | `core/settings.py` |
| ۷ | 🟠 بالا | گزارش موفقیت ارسال پیامک حتی در صورت شکست | `OTP/services/send_sms_service.py:29` |
| ۸ | 🟡 متوسط | نادیده گرفته شدن `start_time`/`end_time` اختصاصی خدمت در محاسبه سانس | `booking/services/calculate_available_slots_service.py` |
| ۹ | 🟡 متوسط | خطای سمت کاربر: تمپلیت اشتباه در ورود مدیر | `admin_panel/views/admin_login_view.py:28` |
| ۱۰ | 🟡 متوسط | انکد ناامن JSON تمپلیت (شکستن با کوتیشن) | `booking/views/select_barber_and_service_view.py:19` |
| ۱۱ | 🟡 متوسط | باگ منطقه زمانی در تاریخ پیش‌فرض (`toISOString`) | `booking/templates/booking/select_datetime.html:88` |
| ۱۲ | 🟡 متوسط | نبود پروفایل مدیر (`AdminPanelModel`) در فلوی ساخت مدیر | `docker-compose.yml:56` |
| ۱۳ | 🟢 پایین | کد مرده و ناسازگاری‌ها (اکشن/سرویس‌های بلااستفاده) | چند فایل |
| ۱۴ | 🟢 پایین | نبود صفحه تاییدیه رزرو و گم شدن `appointment_id` | `booking/templates/booking/review_booking.html:174` |

---

## 🔴 ۱. کرش محاسبه سانس در روزهای چندشیفتی

**فایل:** `apps/booking/services/calculate_available_slots_service.py:36`

```python
working_hours = barbers_models.WorkingHoursModel.objects.get(
    barber_id=barber_id,
    day_of_week=model_day_of_week,
    is_closed=False,
)
```

**مشکل:** از `.get()` استفاده شده، اما سیستم به‌صراحت از **چند شیفت در یک روز** پشتیبانی می‌کند:

- مدل: `WorkingHoursModel` (بدون `unique_together` — در مایگریشن `barbers/0002` حذف شده است).
- سرویس ثبت: `set_barber_working_hours_service.py:23-33` در یک حلقه چند رکورد برای یک روز می‌سازد.
- اکشن فرم: `update_barber_working_hours_action.py:24` روی `zip(start_times, end_times)` حلقه می‌زند و چند شیفت می‌سازد.
- UI: تمپلیت `manage_working_hours.html` دکمه «افزودن شیفت کاری جدید» دارد.

بنابراین اگر آرایشگری برای یک روز ۲ شیفت ثبت کند (مثلاً ۹–۱۳ و ۱۶–۲۰)، این کوئری **`MultipleObjectsReturned`** پرتاب می‌کند. این استثنا در هیچ‌کدام از لایه‌ها هندل نشده:
- در خود سرویس فقط `DoesNotExist` گرفته می‌شود (خط ۴۱).
- اکشن `get_available_slots_action.py` فقط `ValueError` و `TypeError` را می‌گیرد.
→ نتیجه: **خطای ۵۰۰** و از کار افتادن کامل مرحله سوم ویزارد برای آن آرایشگر.

**اصلاح پیشنهادی:** به‌جای `.get()`، همه شیفت‌های روز با `.filter(...).order_by('start_time')` گرفته شوند و حلقه تولید اسلات روی هر شیفت اجرا شود (سانس‌های هر شیفت جدا محاسبه و ادغام شوند). این تغییر باید سمت سرویس انجام شود، نه اکشن (رعایت معماری لایه‌ای).

---

## 🔴 ۲. نبود محدودیت تلاش برای تایید OTP

**فایل:** `apps/OTP/services/verify_otp_service.py:5-14`

```python
otp = models.OTPModel.objects.filter(
    phone_number=phone_number, code=code, is_used=False
).first()
if otp and otp.is_valid(expiry_minutes=2):
```

**مشکل:** کد ۶ رقمی است و پنجره اعتبار ۲ دقیقه، اما **هیچ محدودیتی روی تعداد تلاش اشتباه** وجود ندارد. مهاجم می‌تواند در پنجره اعتبار، هزاران کد را روی یک شماره امتحان کند (۶^۱۰ فقط ۱٬۰۰۰٬۰۰۰ حالت است). همچنین:
- `SendOTPAction` هر بار یک رکورد جدید می‌سازد و کدهای قبلی را باطل نمی‌کند؛ امکان انبوهی رکورد و چند کد فعال هم‌زمان.
- محدودیتی روی تعداد درخواست ارسال (Rate Limit) وجود ندارد → هزینه پیامک و اسپم.

**اصلاح پیشنهادی:** شمارنده تلاش روی رکورد OTP + مسدودسازی موقت پس از N تلاش؛ باطل کردن کدهای قبلی همان شماره هنگام ارسال جدید؛ افزودن throttle روی `SendOTPAction`.

---

## 🟠 ۳. نام خدمت در داشبورد آرایشگر اشتباه است

**فایل:** `apps/barbers/templates/barbers/dashboard.html:53 و 104`

```django
{{ appointment.service.name }}
```

**مشکل:** `AppointmentModel` فیلد `service` **ندارد**؛ رابطه یک‌به‌چند قدیمی در مایگریشن `booking/0002` حذف و به `ManyToMany` با نام `services` تبدیل شده است. بنابراین این عبارت خالی رندر می‌شود (Django خطا نمی‌دهد، ولی ستون «نوع خدمت» در جدول و کارت موبایل همیشه خالی است).

**نکته:** تمپلیت داشبورد مدیر (`admin_panel/dashboard.html:55-57`) این را **درست** پیاده کرده:
```django
{% for barber_service in appointment.services.all %}{{ barber_service.service.name }}{% endfor %}
```

**اصلاح پیشنهادی:** در `barbers/dashboard.html` هم همان الگوی حلقه روی `appointment.services.all` استفاده شود.

---

## 🟠 ۴. رقابت (Race Condition) در ثبت نوبت — دوباره‌رزروی

**فایل:** `apps/booking/services/create_appointment_service.py:54-78`

```python
has_overlap = booking_models.AppointmentModel.objects.filter(...).exists()
if has_overlap:
    raise ValueError(...)
appointment = booking_models.AppointmentModel.objects.create(...)
```

**مشکل:** الگوی «بررسی سپس ثبت» (check-then-act) درون `transaction.atomic()` قرار دارد، اما `transaction.atomic` به‌تنهایی از رقابت جلوگیری نمی‌کند. دو درخواست هم‌زمان که هر دو قبل از `create` بررسی را رد کنند، می‌توانند **هر دو نوبت را ثبت کنند** و اسلات دوبار رزرو شود. (این همان حالتی است که پیام خطای «همین چند لحظه پیش توسط شخص دیگری رزرو شد» برای پوشش آن نوشته شده، اما تضمین واقعی وجود ندارد.)

**اصلاح پیشنهادی:** یکی از موارد زیر:
- قفل ردیف آرایشگر با `select_for_update()` پیش از بررسی تداخل، یا
- قید یکتایی در سطح دیتابیس روی `(barber, date, start_time)` برای نوبت‌های فعال، یا
- سطح ایزولاسیون `SERIALIZABLE` برای این تراکنش.

---

## 🟠 ۵. اکشن‌های قدیمی با امضای نامعتبر (کد مرده‌ی شکسته)

**فایل‌ها:**
- `apps/customers/actions/reserve_appointment_action.py:23`
- `apps/customers/actions/cancel_appointment_action.py:11`

```python
# ReserveAppointmentAction
booking_services.CreateAppointmentService(
    customer=customer, barber=barber, service=service,
    appointment_date=appointment_date, price=price, status='PENDING',
)

# CancelAppointmentAction
booking_services.UpdateAppointmentStatusService(appointment=appointment, status='CANCELLED')
```

**مشکل:** امضای `CreateAppointmentService` اکنون (`user, barber_id, barber_service_ids, booking_date, start_time_str, end_time_str`) است و `UpdateAppointmentStatusService` اکنون (`user, appointment_id, status`). این دو اکشن با پارامترهای قدیمی فراخوانی می‌کنند و در صورت اجرا **`TypeError`** می‌دهند. در حال حاضر هیچ‌کجا استفاده نمی‌شوند (کد مرده)، اما خطرناک‌اند: هر توسعه‌دهنده‌ای ممکن است از آن‌ها استفاده کند و با خطای گیج‌کننده روبه‌رو شود.

**اصلاح پیشنهادی:** حذف این دو فایل و پاک‌سازی importهای مربوطه در `apps/customers/actions/__init__.py` (در حال حاضر هم خالی است و این‌ها را اکسپورت نمی‌کند).

---

## 🟠 ۶. نبود `LOGIN_URL`

**فایل:** `core/settings.py` (تنظیم نشده)

**مشکل:** دکوریتور `@login_required` در `booking/views/review_booking_view.py:10` (و ویوهای پنل آرایشگر) بدون `LOGIN_URL` پیش‌فرض به `/accounts/login/` ریدایرکت می‌کند. این مسیر:
- در `core/urls.py` وجود ندارد (`accounts/` ثبت شده، اما `apps/accounts/urls.py` **خالی** است)،
→ نتیجه: درخواست‌های کاربر لاگین‌نکرده به یک **۴۰۴** می‌رسند، نه صفحه ورود.

**اصلاح پیشنهادی:** تعریف `LOGIN_URL` (مثلاً `booking:otp_page` یا یک صفحه ورود اختصاصی مشتری) در `settings.py`.

---

## 🟠 ۷. گزارش نادرست موفقیت ارسال پیامک

**فایل:** `apps/OTP/services/send_sms_service.py:29` و `apps/OTP/actions/send_otp_action.py:17`

```python
if response:
    return True
return False
```

**مشکل:**
- در صورت بروز استثنا، `return False` می‌شود، اما `SendOTPAction` در هر حالت پیام «کد تایید با موفقیت ارسال شد» را برمی‌گرداند و وضعیت تسک Celery هم بررسی نمی‌شود. کاربر پیام موفقیت می‌بیند در حالی که پیامکی نرسیده است.
- پرینت‌های دیباگ مقادیر حساس را چاپ می‌کنند: `print(username, password)` (خط ۱۴) و `print("Response:", response)` (خط ۲۴). این‌ها باید حذف شوند.

**اصلاح پیشنهادی:** بازگرداندن نتیجه واقعی تا لایه اکشن، ثبت/لاگ خطا، و حذف `print`های حساس.

---

## 🟡 ۸. نادیده گرفته شدن ساعات اختصاصی خدمت

**فایل:** `apps/booking/services/calculate_available_slots_service.py:36-56`

**مشکل:** مدل `BarberServiceModel` فیلدهای `start_time` و `end_time` دارد («ساعت شروع/پایان ارائه خدمت») و در `get_barbers_with_services_service.py:43-44` هم به فرانت‌اند ارسال می‌شود، اما محاسبه سانس فقط از `WorkingHoursModel` استفاده می‌کند و این بازه اختصاصی را **کاملاً نادیده می‌گیرد**. نتیجه: سانس‌هایی نمایش داده می‌شوند که خدمت در آن بازه اصلاً ارائه نمی‌شود.

**اصلاح پیشنهادی:** در محاسبه سانس، بازه مؤثر = اشتراک ساعات کاری روز و بازه اختصاصی خدمت (در صورت وجود).

---

## 🟡 ۹. تمپلیت اشتباه در مسیر خطای ورود مدیر

**فایل:** `apps/admin_panel/views/admin_login_view.py:28`

```python
return render(request, 'accounts/admin_login.html', {'error': result['error']})
```

**مشکل:** تمپلیت `accounts/admin_login.html` وجود ندارد (تمپلیت واقعی `admin_panel/login.html` است). در صورت ورود ناموفق مدیر، **`TemplateDoesNotExist`** رخ می‌دهد. مسیر موفق ورود مشکلی ندارد.

**اصلاح پیشنهادی:** رندر `admin_panel/login.html` همراه با `error`.

---

## 🟡 ۱۰. انکد ناامن JSON در تمپلیت

**فایل:** `apps/booking/views/select_barber_and_service_view.py:19`

```python
'barbers_json': json.dumps(options_data['barbers'], ensure_ascii=False)
```
و در تمپلیت `select_barber_and_service.html:80`:
```javascript
barbers: JSON.parse('{{ barbers_json|safe }}'),
```

**مشکل:** JSON داخل یک رشته با کوتیشن تک‌گانه قرار می‌گیرد. اگر نام یا توضیحات خدمت/آرایشگر شامل `'` باشد (مثلاً متن انگلیسی)، رشته می‌شکند و جاوااسکریپت خطا می‌دهد. همچنین `|safe` بدون `escapejs` در معرض تزریق است.

**اصلاح پیشنهادی:** استفاده از `json_script` جنگو (`{{ barbers|json_script:"barbers-data" }}`) یا حداقل `escapejs` به‌جای درج مستقیم.

---

## 🟡 ۱۱. باگ منطقه زمانی در تاریخ پیش‌فرض

**فایل:** `apps/booking/templates/booking/select_datetime.html:88`

```javascript
const today = new Date().toISOString().split('T')[0];
```

**مشکل:** `toISOString()` تاریخ UTC می‌دهد. با `TIME_ZONE = 'Asia/Tehran'` (UTC+3:30)، برای کاربری که بین نیمه‌شب تا ۰۳:۳۰ بامداد به وقت تهران مراجعه کند، «امروز» اشتباه محاسبه می‌شود (روز قبل). سانس‌های گذشته فیلتر می‌شوند ولی بازه روز اشتباه درخواست می‌شود.

**اصلاح پیشنهادی:** محاسبه تاریخ محلی، مثلاً:
```javascript
const d = new Date();
const today = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
```

---

## 🟡 ۱۲. نبود پروفایل مدیر در فلوی ساخت مدیر

**فایل:** `docker-compose.yml:56`

**مشکل:** کاربر مدیر با `create_superuser('admin', ..., role='MANAGER')` ساخته می‌شود، اما `AdminPanelModel` (پروفایل مدیر با `related_name='manager_profile'`) هیچ‌وقت ساخته نمی‌شود. سرویس `create_admin_profile_service.py` وجود دارد ولی در این فلو فراخوانی نمی‌شود. فعلاً چون ویوها فقط `role`/`is_staff` را چک می‌کنند مشکل کاربری ایجاد نمی‌کند، ولی هر کدی که به `manager_profile` تکیه کند با شکست روبه‌رو می‌شود.

**اصلاح پیشنهادی:** ساخت `AdminPanelModel` هنگام ایجاد کاربر مدیر (در اکشن ثبت‌نام مدیر یا در همان دستور اولیه).

---

## 🟢 ۱۳. کد مرده و ناسازگاری‌ها

- `apps/barbers/actions/WorkingHoursServices/set_barber_working_hours_action.py` — امضایش (`day_of_week, start_time, end_time, slot_duration`) با سرویس (`shifts: list`) نمی‌خواند و **هیچ‌گاه استفاده نمی‌شود**؛ اکشن واقعی `UpdateBarberWorkingHoursAction` است. اکشن مرده را حذف و از `actions/__init__.py` پاک کنید.
- `apps/booking/services/check_slot_availability_service.py` — `CheckSlotAvailabilityService` وجود دارد اما استفاده نمی‌شود؛ منطق تداخل در `CreateAppointmentService` **تکرار** شده (نقض DRY). بهتر است `CreateAppointmentService` از همین سرویس استفاده کند.
- `apps/barbers/actions/BarberServiceActions/assign_barber_service_action.py` و `add_barber_service_service.py` — مسیر جایگزین منطق `UpdateOrCreateBarberServiceService` هستند؛ دو پیاده‌سازی موازی برای یک کار.
- `apps/OTP/models.py` — یک فایل خالی است که با پکیج `models/` تداخل دارد (کد مرده). پیشنهاد حذف.
- ناسازگاری در تعیین «امروز»: `GetBarberTodayAppointmentsAction` از `timezone.now().date()` و `GetTodayAppointmentsService` از `date.today()` استفاده می‌کند. یکسان‌سازی توصیه می‌شود.
- `AppointmentModel` هیچ قید یکتایی یا `index` روی `(barber, date, status)` ندارد؛ با رشد داده، کوئری‌های بررسی تداخل کند می‌شوند.

---

## 🟢 ۱۴. تجربه کاربری و فلوی نهایی

- پس از ثبت موفق نوبت، `review_booking.html:174` کاربر را به `/` (لندینگ) می‌فرستد و `appointment_id` بازگشتی استفاده نمی‌شود. طبق `appointment_std.md` قرار بود صفحه «تاییدیه رزرو» نمایش داده شود.
- در همان فایل (خط ۱۱۰) در صورت ناقص بودن اطلاعات به `booking:select-barber` ریدایرکت می‌شود؛ خوب است، اما هیچ صفحه «نوبت‌های من» برای مشتری وجود ندارد (سرویس `GetCustomerAppointmentsService` هست، ویو/تمپلیت نیست).
- Alpine.js از CDN بارگذاری می‌شود؛ در حالت آفلاین یا CSP سخت‌گیرانه، کل ویزارد از کار می‌افتد.

---

## نکات معماری (نه باگ، اما مهم)

1. **صحت لایه‌بندی:** فلوی اصلی رزرو (OTP، انتخاب آرایشگر/خدمت، انتخاب زمان، ثبت) لایه‌بندی `View → Action → Service` را **درست** رعایت کرده است. استثناها:
   - `SaveSalonServiceView` (خط ۲۵) و ویوهای پنل، `request.POST` را مستقیم به اکشن می‌دهند (اکشن‌های پنل، مثل `CreateSalonServiceAction`، داده را پارس نشده تحویل می‌گیرند).
   - در `SelectDatetimeView` اعتبارسنجی/پارس در ویو انجام می‌شود و اکشن دوباره پارس می‌کند (تکرار).
2. **تست:** فایل‌های `tests.py` در همه اپ‌ها **خالی** هستند. برای فلوی حساسی مثل نوبت‌دهی (تداخل زمانی، رقابت، مرزهای تاریخ/ساعت، اعتبار OTP) تست خودکار وجود ندارد. این بزرگ‌ترین شکاف پروژه است و باگ‌های ۱ و ۴ به‌سادگی با تست پوشش داده می‌شدند.

---

## ترتیب پیشنهادی رفع

1. **بحرانی فوری:** مورد ۱ (کرش چندشیفتی) و مورد ۲ (امنیت OTP).
2. **بالا (صحت/امنیت):** موارد ۳، ۴، ۵، ۶، ۷.
3. **متوسط (تجربه/پایداری):** موارد ۸، ۹، ۱۰، ۱۱، ۱۲.
4. **پاک‌سازی:** موارد ۱۳ و ۱۴ و افزودن تست‌های فلوی رزرو.

---

## پیوست: خلاصه فایل‌های درگیر

| فایل | موارد مرتبط |
| --- | --- |
| `apps/booking/services/calculate_available_slots_service.py` | ۱، ۸ |
| `apps/OTP/services/verify_otp_service.py` | ۲ |
| `apps/OTP/services/send_sms_service.py` | ۷ |
| `apps/barbers/templates/barbers/dashboard.html` | ۳ |
| `apps/booking/services/create_appointment_service.py` | ۴، ۱۳ |
| `apps/customers/actions/reserve_appointment_action.py` | ۵ |
| `apps/customers/actions/cancel_appointment_action.py` | ۵ |
| `core/settings.py` | ۶ |
| `apps/admin_panel/views/admin_login_view.py` | ۹ |
| `apps/booking/views/select_barber_and_service_view.py` | ۱۰ |
| `apps/booking/templates/booking/select_datetime.html` | ۱۱ |
| `docker-compose.yml` | ۱۲ |
| `apps/barbers/actions/WorkingHoursServices/set_barber_working_hours_action.py` | ۱۳ |
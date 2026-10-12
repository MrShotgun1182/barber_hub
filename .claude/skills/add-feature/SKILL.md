# اسکیل: افزودن قابلیت جدید

هر قابلیت جدید باید طبق معماری لایه‌ای `View → Action → Service → Model` پیاده شود.
این اسکیل مسیر گام‌به‌گام ساخت فایل‌ها را مشخص می‌کند تا هیچ لایه یا `__init__.py` فراموش نشود.

## نکات طلایی (قبل از شروع)

- جریان داده یک‌طرفه است: ویو فقط اکشن صدا می‌زند، اکشن فقط سرویس، سرویس فقط Model/ORM.
- زبان همه‌چیز فارسی است: docstring، `verbose_name`، پیام خطا، کامنت. نام متغیر/تابع انگلیسی.
- اجرای پروژه فقط با Docker Compose مجاز است (`docker compose up --build`). اجرای لوکال روی سیستم میزبان (`runserver`، Celery، npm) ممنوع است — دستورات را داخل کانتینر اجرا کن. جزئیات در اسکیل `run-stack`.
- اپ‌ها با نام خالی import می‌شوند (`from booking import services as booking_services`) چون `apps/` روی `sys.path` است. هرگز `apps.` نگذار.
- در `admin_panel` پوشه اکشن‌ها `Actions/` است (حرف بزرگ)؛ در بقیه اپ‌ها `actions/`.
- فایل‌ها snake_case با پسوند لایه؛ توابع اصلی PascalCase (حتی ویوها، که تابع هستند نه کلاس).

## گام‌ها (به ترتیب)

۱. **مدل (در صورت نیاز)** — `apps/<app>/models/<name>_model.py` با کلاس `<Name>Model`.
   - آن را در `models/__init__.py` همان اپ re-export کن.
   - `makemigrations` بگیر. برای فیلدهای تاریخ/وضعیت، `verbose_name` فارسی و `db_index` در صورت کوئری مکرر.
   - مدل را در `admin.py` اپ ثبت کن (به سبک اپ‌های موجود نگاه کن).

۲. **سرویس‌ها** — `apps/<app>/services/<action>_<name>_service.py` با تابع `<Action><Name>Service`.
   - سرویس منطق خالص دیتابیس/محاسبات است؛ `request` دریافت نکند.
   - Type hint بده: `barber_id: int, barber_service_ids: list[int] -> dict`.
   - docstring فارسی یک‌خطی که نقش لایه را بگوید.
   - ثبت در `services/__init__.py`.

۳. **اکشن** — `apps/<app>/actions/<operation>_<name>_action.py` با تابع `<Operation><Name>Action`.
   - اکشن خطاها را خودش catch کند و `dict` برگرداند؛ الگوی غالب: `{'status': 'success'|'error', 'message': ...}`.
     برای عملیات‌های اتوریکیشن ورود، قرارداد هم‌خانواده‌اش را ببین (برخی `success`/`error` بولی دارند).
   - عملیات چندگانه/اتمیک را با `transaction.atomic()` بپوشان.
   - ثبت در `actions/__init__.py`.

۴. **ویو** — `apps/<app>/views/<name>_view.py` با تابع `<Name>View`.
   - ویو فقط request را می‌پارسد، اکشن را صدا می‌زند، و نتیجه را render یا `JsonResponse` می‌کند.
   - هیچ ORM و هیچ فراخوانی مستقیم سرویس در ویو ممنوع.
   - اگر پنل است، `@login_required` + بررسی دستی نقش (`request.user.role`) فراموش نشود.
   - ثبت در `views/__init__.py`.

۵. **مسیر** — `urls.py` اپ: `path('...', views.<Name>View, name='<name>')`. اگر اپ `urls.py` ندارد (مثل `OTP`، `customers`، `salon_services`)، ویو از طریق اپ دیگر (معمولاً `booking`) استفاده می‌شود.

۶. **تمپلیت** — `apps/<app>/templates/<app>/<name>.html`؛ ارث‌بری از `core/base.html` (یا `barber_base`/`admin_base` برای پنل‌ها).

۷. **فront-end** — اگر کلاس Tailwind جدیدی استفاده کردی، کامپایلر باید در حال اجرا باشد (`cd frontend && npm run dev`) تا `frontend/static/dist/output.css` به‌روز شود.

۸. **اعتبارسنجی زمان** — اگر با نوبت/اسلات کاری داری: تداخل = `max(start1, start2) < min(end1, end2)`؛ فقط نوبت‌های `PENDING` و `CONFIRMED` اسلات را اشغال می‌کنند؛ `day_of_week` با نگاشت `(date.weekday() + 2) % 7`.

۹. در پایان: `python manage.py makemigrations` (در صورت تغییر مدل) و `python manage.py test` را اجرا کن و نتیجه را گزارش بده.

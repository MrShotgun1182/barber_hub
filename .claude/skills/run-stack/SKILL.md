# اسکیل: اجرای استک پروژه

راه‌اندازی و اجرای Barber Hub برای تست دستی تغییرات.

## قانون سخت

**اجرای پروژه فقط و فقط با Docker Compose مجاز است.**

```bash
docker compose up --build
```

اجرای لوکال خارج از Docker Compose — یعنی `python manage.py runserver`، اجرای مستقیم Celery worker (`celery -A core worker`) یا اجرای مستقیم `npm run dev` / `npm run build` روی سیستم میزبان — **ممنوع** است. همه اجزا (وب، PostgreSQL، Redis، Celery) باید از طریق `docker compose up` بالا بیایند.

اگر برای تست لازم است دستوری داخل پروژه اجرا شود، آن را داخل کانتینر اجرا کن، مثلاً:

```bash
# اجرای تست‌ها داخل کانتینر
docker compose exec web python manage.py test

# ساخت مایگریشن داخل کانتینر
docker compose exec web python manage.py makemigrations
```

(نام سرویس وب را با نام واقعی در `docker-compose.yml` تطبیق بده.)

## کامپایل Tailwind

اگر کلاس Tailwind جدیدی به تمپلیت‌ها اضافه شد، خروجی باید به `frontend/static/dist/output.css` کامپایل شود تا در تمپلیت‌ها با `{% static 'dist/output.css' %}` لود شود. این کار را هم در چارچوب Docker انجام بده (به‌عنوان مثال، اجرای build داخل کانتینر یا اسکریپت موجود در `docker-compose.yml`) — نه با اجرای مستقیم npm روی سیستم میزبان.

## پیش‌نیازها

- Docker و Docker Compose نصب باشند.
- اعتبارنامه‌های پیامک از `.env`: `MELIPAYAMAK_USERNAME`, `MELIPAYAMAK_PASSWORD`, `MELIPAYAMAK_FROM`.
- در حالت توسعه، `SendSMSService` در `apps/OTP` دارای print دیباگ است که کد OTP را چاپ می‌کند — برای تست می‌توانی کد را از لاگ کانتینر بخوانی (`docker compose logs -f <celery-service>`).

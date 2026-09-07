import os
from celery import Celery

# تنظیم پیش‌فرض settings جنگو برای Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('barber_hub')

# لود کردن تنظیماتی که با پیشوند CELERY_ در settings.py تعریف کردیم
app.config_from_object('django.conf:settings', namespace='CELERY')

# شناسایی خودکار تمام فایل‌های tasks.py در اپلیکیشن‌ها (مثل OTP/tasks.py)
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
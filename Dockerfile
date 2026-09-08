# ۱. استفاده از میرور داکر برای دریافت ایمیج پایه پایتون
FROM mirror-docker.runflare.com/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب Node.js و npm
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل‌های requirements و تنظیم میرور pip برای نصب سریع پکیج‌های پایتون
COPY requirements.txt /app/
RUN pip config set global.index-url https://mirror-pypi.runflare.com/simple \
    && pip config set global.trusted-host mirror-pypi.runflare.com \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# کپی کل پروژه
COPY . /app/

# ۲. تنظیم میرور npm، نصب وابستگی‌های فرانت‌اند و Build اولیه Tailwind
WORKDIR /app/frontend
RUN npm config set registry https://mirror-npm.runflare.com \
    && npm config set strict-ssl false \
    && npm install \
    && npm run build

# برگشت به دایرکتوری اصلی
WORKDIR /app

EXPOSE 8000

# اجرای سرور توسعه جنگو
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
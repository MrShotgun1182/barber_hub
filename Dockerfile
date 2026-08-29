FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب Node.js و npm
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل‌های requirements و نصب پکیج‌های پایتون
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# کپی کل پروژه
COPY . /app/

# نصب وابستگی‌های Node.js و Build اولیه Tailwind
WORKDIR /app/frontend
RUN npm install && npm run build

# برگشت به دایرکتوری اصلی
WORKDIR /app

EXPOSE 8000

# از CMD به جای ENTRYPOINT استفاده می‌کنیم چون در compose command داریم
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
با توجه به درخواست شما برای افزودن لایه اکشن (Action Layer) به عنوان یک لایه میانی بین ویو و سرویس، فایل مستند را به‌روزرسانی می‌کنم. این لایه جدید وظیفه ارکستراسیون (Orchestration) و ترکیب چندین سرویس برای انجام یک عملیات خاص را بر عهده خواهد داشت.

---

# مستند فنی ساختار و معماری پروژه‌های جنگو (Django & Tailwind Architecture Guide)

این مستند استاندارد ساختار درختی، لایه‌بندی، مدیریت فرانت‌اند و قواعد نام‌گذاری (Naming Conventions) را در پروژه‌های جنگو تبیین می‌کند. هدف این معماری، تفکیک کامل وظایف (Separation of Concerns)، سادگی کدها با متدولوژی توابع مجزا و یکپارچه‌سازی مدرن ابزارهای فرانت‌اند است.

## ۱. ساختار درختی پروژه (Project Directory Tree)

ساختار کلی پروژه به سه بخش اصلی تقسیم می‌شود:
۱. **`core`**: تنظیمات ریشه و اصلی جنگو.
۲. **`apps`**: لایه‌ها و اپلیکیشن‌های بک‌اند پروژه به صورت ماژولار.
۳. **`frontend`**: محیط کاملاً مستقل برای ابزارهای فرانت‌اند (NPM، فایل‌های استاتیک خام و کانفیگ Tailwind).

```text
my_project/
│
├── core/                         # تنظیمات اصلی پروژه
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
│
├── apps/                         # پوشه مرجع تمام لایه‌ها و اپ‌های بک‌اند
│   │
│   └── accounts/                 # نمونه یک اپلیکیشن (مثلاً مدیریت کاربران)
│       ├── __init__.py
│       ├── apps.py
│       │
│       ├── models/               # پوشه مدل‌های دیتابیس
│       │   ├── __init__.py
│       │   └── account_model.py
│       │
│       ├── views/                # پوشه ویوهای جنگو (توابع پاسکال‌کیس)
│       │   ├── __init__.py
│       │   └── home_view.py
│       │
│       ├── actions/              # لایه اکشن (ارکستراسیون بین ویو و سرویس)
│       │   ├── __init__.py
│       │   └── user_login_action.py
│       │
│       ├── services/             # لایه توابع ارتباط با دیتابیس و منطق
│       │   ├── __init__.py
│       │   └── get_account_service.py
│       │
│       └── templates/            # پوشه تمپلیت‌های محلی این اپ
│           └── accounts/         # پوشه هم‌نام با اپ برای جلوگیری از تداخل نام
│               └── home.html
│
├── frontend/                     # لایه مستقل فرانت‌اند و مدیریت Tailwind
│   ├── node_modules/             # پکیج‌های نصب شده توسط npm
│   ├── src/                      # فایل‌های CSS و استایل‌های خام ورودی تیلویند
│   │   └── input.css
│   ├── package.json              # مدیریت اسکریپت‌های کامپایل تیلویند
│   └── tailwind.config.js        # کانفیگ و تنظیمات اختصاصی Tailwind
│
├── static/                       # خروجی نهایی کامپایل‌شده استاتیک‌ها (CSSهای نهایی)
│   └── css/
│       └── output.css            # فایلی که تیلویند خروجی می‌دهد و در قالب‌ها لود می‌شود
│
├── templates/                    # پوشه تمپلیت‌های سراسری پروژه (مثل base.html)
│   └── base.html
│
└── manage.py

```

---

## ۲. تنظیمات مسیردهی سیستم و تمپلیت‌ها (`settings.py`)

برای حذف تکرار کلمه `apps` در زمان ثبت و آدرس‌دهی اپ‌ها، مدیریت تمپلیت‌های سراسری پروژه و تنظیمات فایل‌های استاتیک خروجی تیلویند، پیکربندی زیر در فایل `settings.py` قرار می‌گیرد:

```python
import sys
from pathlib import Path

# مسیر ریشه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# اضافه کردن پوشه apps به مسیرهای سیستم برای آدرس‌دهی مستقیم اپ‌ها
sys.path.insert(0, str(BASE_DIR / 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # اپلیکیشن‌های پروژه بدون نیاز به پیشوند apps
    'accounts',  
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # تعریف پوشه تمپلیت سراسری در ریشه پروژه (برای فایل‌هایی مثل base.html)
        'DIRS': [BASE_DIR / 'templates'],
        # فعال بودن شناسایی خودکار پوشه templates درون هر اپلیکیشن
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# تنظیمات استاتیک برای خواندن خروجی کامپایل شده تیلویند
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

```

---

## ۳. قواعد نام‌گذاری فایل‌ها و توابع (Naming Conventions)

* **نام فایل‌ها (Snake Case):** نام هر فایل به‌صورت حروف کوچک بوده و در انتهای آن نوع لایه و پوشه‌ای که در آن قرار دارد (مانند `_service`، `_action` یا `_view`) ذکر می‌شود.
* **نام توابع داخلی (Pascal Case):** درون فایل‌های ویو، اکشن و سرویس، تابع اصلی به عنوان نقطه ورود (Entry Point) با فرمت PascalCase تعریف می‌شود تا از توابع جانبی متمایز باشد.

### جدول راهنمای نام‌گذاری:

| لایه (پوشه) | قاعده نام‌گذاری فایل (Snake Case) | قاعده نام‌گذاری تابع یا کلاس اصلی | نمونه بارز مسیر فایل و نام تابع |
| --- | --- | --- | --- |
| **Models** | `[name]_model.py` | `[Name]Model` (کلاس مدل جنگو) | `account_model.py` / `AccountModel` |
| **Services** | `[action]_[name]_service.py` | `[Action][Name]Service` (تابع اصلی) | `get_account_service.py` / `GetAccountService` |
| **Actions** | `[operation]_[name]_action.py` | `[Operation][Name]Action` (تابع اصلی) | `user_login_action.py` / `UserLoginAction` |
| **Views** | `[name]_view.py` | `[Name]View` (تابع اصلی) | `home_view.py` / `HomeView` |
| **Templates** | `[name].html` | - | `templates/accounts/home.html` |

---

## ۴. ساختار کانفیگ Tailwind CSS در پوشه فرانت‌اند

برای اینکه لایه فرانت‌اند بتواند کلاس‌های استفاده‌شده در فایل‌های HTML (چه در پوشه ریشه و چه درون اپلیکیشن‌ها) را به درستی پایش (Watch) و کامپایل کند، فایل `frontend/tailwind.config.js` به صورت زیر تنظیم می‌شود:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // پایش تمپلیت‌های سراسری پروژه
    "../templates/**/*.html",
    // پایش تمام تمپلیت‌های داخلی پوشه apps
    "../apps/**/templates/**/*.html",
    // پایش فایل‌های جاوااسکریپت احتمالی در فرانت‌اند
    "./src/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

```

> **نکته کامپایل استایل‌ها:** در فایل `package.json` واقع در پوشه `frontend`، اسکریپت ساخت استایل‌ها به گونه‌ای تنظیم می‌شود که خروجی نهایی را مستقیماً در پوشه static ریشه پروژه بسازد:
> `"build": "tailwindcss -i ./src/input.css -o ../static/css/output.css --watch"`

---

## ۵. نمونه پیاده‌سازی جریان داده و رندر تمپلیت (Code Example Flow)

### الف) لایه سرویس (`apps/accounts/services/get_account_service.py`)

```python
from accounts.models.account_model import AccountModel

def GetAccountService(account_id: int) -> AccountModel:
    """
    تابع خالص لایه سرویس برای گرفتن داده از دیتابیس
    """
    try:
        return AccountModel.objects.get(id=account_id)
    except AccountModel.DoesNotExist:
        return None

```

### ب) لایه سرویس احراز هویت (`apps/accounts/services/authenticate_user_service.py`)

```python
from django.contrib.auth import authenticate

def AuthenticateUserService(username: str, password: str):
    """
    سرویس احراز هویت کاربر
    """
    user = authenticate(username=username, password=password)
    return user

```

### ج) لایه اکشن (`apps/accounts/actions/user_login_action.py`)

```python
from accounts.services.get_account_service import GetAccountService
from accounts.services.authenticate_user_service import AuthenticateUserService
from django.contrib.auth import login

def UserLoginAction(request, username: str, password: str) -> dict:
    """
    تابع لایه اکشن برای ارکستراسیون فرآیند ورود کاربر
    این تابع چندین سرویس را ترکیب کرده و یک عملیات کامل را انجام می‌دهد
    """
    result = {
        'success': False,
        'user': None,
        'error': None
    }
    
    # احراز هویت کاربر با استفاده از سرویس مربوطه
    user = AuthenticateUserService(username, password)
    
    if user is not None:
        # ورود کاربر به سیستم
        login(request, user)
        
        # دریافت اطلاعات کامل حساب کاربری
        account_data = GetAccountService(user.id)
        
        result['success'] = True
        result['user'] = user
        result['account'] = account_data
    else:
        result['error'] = 'نام کاربری یا رمز عبور اشتباه است'
    
    return result

```

### د) لایه ویو (`apps/accounts/views/login_view.py`)

```python
from django.shortcuts import render, redirect
from accounts.actions.user_login_action import UserLoginAction

def LoginView(request):
    """
    تابع لایه ویو برای مدیریت درخواست ورود کاربر
    ویو فقط اکشن مربوطه را فراخوانی می‌کند و نیازی به صدا زدن مستقیم سرویس‌ها ندارد
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # فراخوانی اکشن ورود کاربر - تمام منطق در اکشن کپسوله شده است
        result = UserLoginAction(request, username, password)
        
        if result['success']:
            return redirect('home')
        else:
            context = {
                'error': result['error']
            }
            return render(request, 'accounts/login.html', context)
    
    return render(request, 'accounts/login.html')

```

### ه) لایه ویو نمایش خانه (`apps/accounts/views/home_view.py`)

```python
from django.shortcuts import render
from accounts.actions.get_user_dashboard_action import GetUserDashboardAction

def HomeView(request):
    """
    تابع لایه ویو برای مدیریت درخواست و رندر تمپلیت با الگوی کپسوله‌سازی
    """
    # فراخوانی اکشن برای دریافت اطلاعات داشبورد کاربر
    dashboard_data = GetUserDashboardAction(request.user)
    
    context = {
        'dashboard': dashboard_data
    }
    
    # ارجاع به تمپلیت اختصاصی اپلیکیشن با الگوی Namespace
    return render(request, 'accounts/home.html', context)

```

### و) تمپلیت اصلی پروژه (`templates/base.html`)

تمام تمپلیت‌های محلی اپ‌ها از این فایل ارث‌بری می‌کنند و فایل CSS نهایی تیلویند در این بخش لود می‌شود:

```html
{% load static %}
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}پروژه من{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/output.css' %}">
</head>
<body class="bg-gray-100 text-gray-900">
    {% block content %}
    {% endblock %}
</body>
</html>

```

---

## ۶. توضیحات تکمیلی لایه اکشن (Action Layer)

لایه اکشن به عنوان یک لایه میانی بین ویو و سرویس عمل می‌کند و وظایف زیر را بر عهده دارد:

### ۶.۱. ارکستراسیون سرویس‌ها (Service Orchestration)
- ترکیب چندین سرویس مختلف برای انجام یک عملیات کامل
- مدیریت ترتیب و وابستگی‌های بین سرویس‌ها

### ۶.۲. کپسوله‌سازی منطق کسب‌وکار (Business Logic Encapsulation)
- پیاده‌سازی سناریوهای پیچیده کسب‌وکار که نیاز به چندین سرویس دارند
- ایجاد یک نقطه ورود واحد برای هر عملیات تجاری

### ۶.۳. مدیریت تراکنش‌ها (Transaction Management)
- کنترل تراکنش‌های دیتابیس در سطح عملیات
- اطمینان از یکپارچگی داده‌ها در عملیات‌های چند مرحله‌ای

### ۶.۴. مزایای استفاده از لایه اکشن:
- **کاهش پیچیدگی ویوها:** ویوها فقط یک اکشن را فراخوانی می‌کنند
- **قابلیت استفاده مجدد:** اکشن‌ها می‌توانند در ویوهای مختلف مورد استفاده قرار گیرند
- **تست‌پذیری بالاتر:** تست کردن منطق کسب‌وکار به صورت مجزا آسان‌تر است
- **شفافیت بیشتر:** جریان داده و مسئولیت‌ها به وضوح مشخص می‌شوند
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-6+3slwc$259dkg^1*tv498%evsc*3=lt9v#z*vru)mtjwzo_h9'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
os.sys.path.insert(0, str(BASE_DIR / 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'barbers',
    'customers',
    'admin_panel',
    'booking',
    'salon_services',
    'OTP',
]

AUTH_USER_MODEL = 'accounts.UserModel'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database Configuration (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'barber_db'),
        'USER': os.environ.get('DB_USER', 'barber_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'barber_pass'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.normpath(os.path.join(BASE_DIR, 'frontend', 'static')),
]
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

load_dotenv(BASE_DIR / '.env')

# خواندن اطلاعات پنل پیامک
MELIPAYAMAK_USERNAME = os.getenv('MELIPAYAMAK_USERNAME')
MELIPAYAMAK_PASSWORD = os.getenv('MELIPAYAMAK_PASSWORD')
MELIPAYAMAK_FROM = os.getenv('MELIPAYAMAK_FROM')

# ==============================================================================
# ⚡ Celery & Redis Configuration
# ==============================================================================
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
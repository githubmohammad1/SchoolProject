
from pathlib import Path
from mongoengine import connect
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-fallback-key-for-dev')
from datetime import timedelta




DEBUG = True

ALLOWED_HOSTS = ['*'] # يجب تغييرها لنطاق الإنتاج لاحقاً
CORS_ALLOWED_ORIGINS = []
# 4. إعداد الـ HASHERS (تجزئة كلمات المرور)
# 2. إعداد الـ HASHERS (تجزئة كلمات المرور)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher', 
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    # ...
]


TEMPLATES = [
    {
        # ... إعدادات أخرى ...
        'DIRS': [BASE_DIR / 'templates'], # تأكد من وجود هذا السطر إذا كان المجلد في جذر المشروع
        'APP_DIRS': True, # هذا يسمح لـ Django بالبحث في مجلد templates داخل كل تطبيق (core)
        # ...
    },
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
'rest_framework',         # مطلوب لـ DRF
    'rest_framework_simplejwt', # مطلوب لـ JWT
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SchoolProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SchoolProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ====== إعدادات MongoDB ======


# يتم الاتصال بقاعدة بيانات MongoDB (نفترض أنها تعمل على المنفذ الافتراضي 27017)
MONGO_DATABASE_NAME = 'school_mongo_db' # اسم قاعدة بيانات MongoDB الخاصة بنا

connect(
    db=MONGO_DATABASE_NAME,
    host='localhost',
    port=27017  # المنفذ الافتراضي لـ MongoDB
)


# 3. إعدادات JWT (كما كانت سابقاً)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}



from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    # ...
}







# =============================
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url  # مكتبة للربط بقواعد البيانات السحابية
from mongoengine import connect # إذا كنت مصرّاً على استخدام MongoDB بجانب SQL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================
# إعدادات الأمان والبيئة (Production vs Local)
# ==============================================

# جلب المفتاح السري من متغيرات البيئة، أو استخدام قيمة افتراضية للتطوير فقط
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me-please-local-key')

# اجعلها True فقط إذا لم يتم تحديدها كـ False في السيرفر (للأمان)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# السماح لجميع النطاقات مؤقتاً للنسخة التجريبية
ALLOWED_HOSTS = ['*']

# ==============================================
# التطبيقات المثبتة
# ==============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # تطبيقات الطرف الثالث
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',  # هام جداً للربط مع الفرونت إند
    'drf_yasg',
    # تطبيقك
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- ضروري جداً للمخدمات المجانية (لملفات CSS/JS)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',       # <--- يجب أن يكون قبل CommonMiddleware
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
        'DIRS': [BASE_DIR / 'templates'], # دمجنا الإعدادات هنا
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

WSGI_APPLICATION = 'SchoolProject.wsgi.application'

# ==============================================
# إعدادات قواعد البيانات (SQL Database)
# ==============================================

# المخدمات المجانية مثل Render تستخدم PostgreSQL
# هذا الكود يختار تلقائياً بين SQLite (محلياً) و PostgreSQL (على السيرفر)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# ==============================================
# إعدادات MongoDB (إذا كنت تستخدمها فعلياً)
# ==============================================

# ملاحظة: الكود السابق الذي كتبناه يعتمد كلياً على Django ORM (SQL)
# إذا كنت تحتاج MongoDB لأشياء أخرى، نستخدم متغير بيئة للاتصال بـ Atlas MongoDB
MONGO_URI = os.environ.get('MONGO_URI') 
if MONGO_URI:
    connect(host=MONGO_URI)
else:
    # الاتصال المحلي عند التطوير
    try:
        connect(db='school_mongo_db', host='localhost', port=27017)
    except:
        pass # تجاهل الخطأ إذا لم تكن MongoDB مثبتة محلياً

# ==============================================
# إعدادات التشفير والتحقق
# ==============================================

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================
# التدويل والوقت
# ==============================================

LANGUAGE_CODE = 'ar-sa' # تم التغيير للعربية
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================
# الملفات الثابتة (Static Files)
# ==============================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# ضغط وتخزين الملفات لتعمل على السيرفر
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================
# إعدادات REST Framework & JWT
# ==============================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # تم زيادة الوقت قليلاً
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # استخدام نفس مفتاح التطبيق
}

# ==============================================
# إعدادات CORS (للربط مع المتصفحات والموبايل)
# ==============================================

# في الإصدار التجريبي نسمح للجميع
CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS = True
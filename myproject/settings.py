"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pssafmt1ntht3v_=yx0tk12hmt8lm&0+9gboxr!1)(gd7vy*#='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'shaarp3',
    'Espan',
    'France',
    'Netherlandss',
    'germanyapp',
    'corsheaders',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
  # Ensure this is enabled for CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'Espan': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'es.sqlite3',
    },
    'France': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'fr.sqlite3',
    },
    'Netherlands': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'nd.sqlite3',
    },
    'Germany': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'de.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'support@sharplogician.com'
EMAIL_HOST_PASSWORD = 'tnhb sddw fbee ejkw'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATABASE_ROUTERS = [
    'myproject.db_routers.EspanRouter',
    'myproject.db_routers.FranceRouter',
    'myproject.db_routers.NetherlandsRouter',
    'myproject.db_routers.GermanyRouter',

]

CORS_ALLOW_HEADERS = [
    'content-type',
    'x-super-admin',  # Allow your custom header
    'authorization',
    'accept',
    'origin',
    'x-requested-with',
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3001', 
    
    # Replace with your Next.js frontend URL
    'http://localhost:3000',
    'http://127.0.0.1:8000',
    'https://sharplogicians.com',
    'https://sharplogicians.fr',
    'https://sharplogicians.de',
    'https://sharplogicians.nl',
    'https://sharplogicians.en',
    'http://157.230.211.231:3006',




   
    # Replace with your Next.js frontend URL
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/api/static/'
MEDIA_URL = 'api/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB
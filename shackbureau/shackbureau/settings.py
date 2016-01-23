"""
Django settings for shackbureau project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nw507n4+9-1xmu&lx$4q!qc2)mzfrr8xv*6*19#z$h8t)+x*qe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'django_extensions',
    'localflavor',
    'reversion',
    ## own apps
    'usermanagement',
    'districtcourt',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'shackbureau.urls'

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

WSGI_APPLICATION = 'shackbureau.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shackbureau',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

if os.environ.get('TEST_ON_PLATFORM', '').lower() == 'wercker':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', '127.0.01'),
            'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT', '5432'),
            'NAME': os.environ.get('POSTGRES_ENV_POSTGRES_USER'),
            'USER': os.environ.get('POSTGRES_ENV_POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_ENV_POSTGRES_PASSWORD'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, 'static')),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))

EXPORT_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'export'))

# set email to stdout for debugging
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .production_settings_template import *
except ImportError as e:
    pass

try:
    from .production_settings import *
except ImportError as e:
    pass

# -*- coding: utf-8 -*-

import os
from configparser import RawConfigParser
from django.utils.translation import ugettext_lazy as _

config = RawConfigParser()
config.read('/etc/secrets/metropol_settings.ini')

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST'),
        'PORT': config.get('database', 'DATABASE_PORT'),
        'TEST': {
            'NAME': config.get('database', 'TEST_DATABASE_NAME'),
        },
    }
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secrets', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('debug', 'DEBUG')

ALLOWED_HOSTS = [host for host in config.get('debug', 'ALLOWED_HOSTS').split(',')]

FILE_CHARSET = 'UTF-8'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'metropol_abogados',
    'bootstrap3',
    'endless_pagination'
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

ROOT_URLCONF = 'metropol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "/metropol_abogados/templates")],
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

WSGI_APPLICATION = 'metropol.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


# Login
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

# Transactions
ATOMIC_REQUESTS = True

# I18N
USE_I18N = True

LANGUAGES = [
    ('es', _('Spanish')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)


# Bootstrap 3 settings

BOOTSTRAP3 = {
    # The URL to the jQuery JavaScript file
    'jquery_url': '%sjs/jquery-2.1.4.min.js' % STATIC_URL,
    'include_jquery': True,
    # The Bootstrap base URL
    'base_url': '%s' % STATIC_URL,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-3',

    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',

    # Set HTML required attribute on required fields
    'set_required': False,

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': '',

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': '',
}

DATE_INPUT_FORMATS = ('%d/%m/%Y',)
DATE_FORMAT = 'd/m/Y'
FILE_CHARSET = 'ISO-8859-1'
DEFAULT_CHARSET = 'ISO-8859-1'

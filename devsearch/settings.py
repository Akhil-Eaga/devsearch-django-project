"""
Django settings for devsearch project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3^e(9g14jl9nx2s04ss*xg)_q3o8it+z-2&8s$_^&g1f2$#3&*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'projects.apps.ProjectsConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'devsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'devsearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Configuration to send emails from the app to the user
# EAMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587 # this port is for using TLS
# EMAIL_HOST_USER = "random.email@gmail.com"
# EMAIL_HOST_PASSWORD = "should_use_an_app_password_here"


# TRYING OUT THE AMAZON AWS SES (SIMPLE EMAIL SERIVICE) SMTP TO GET THE EMAILS WORKING
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIASJERNDLOSCXYAQHZ'
AWS_SECRET_ACCESS_KEY = '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'

# used by the send_mail function in signals.py to use as the from address for sending emails
EMAIL_HOST_USER = 'gojohnygo2013@gmail.com'

# this is added to handle the case where django itself sends email from the email address webmaster@localhost
# but since we are using AWS 
DEFAULT_FROM_EMAIL = 'gojohnygo2013@gmail.com'


# SOME SUPPORT LINKS
# https://stackoverflow.com/questions/37528301/email-address-is-not-verified-aws-ses


# NOTES FOR USING AWS SES SERVICE TO SEND EMAILS
# BY DEFAULT SES WORKS FROM A SANDBOX AND WHILE THE SERVICE IS IN SANDBOX, 
# BOTH THE FROM EMAIL AND TO EMAIL SHOULD BE VERIFIED IN THE AWS CONSOLE
# BUT IF YOU MOVE TO PRODUCTION (COMING OUT OF SANDBOX), TO ADDRESSES NEED NOT BE VERIFIED



# for some reason, when I configured this with my own email and password, it was giving a TimeOut Error
# mostly due to the security settings not allowing app passwords and less secure app permission at the same time
# the following stackoverflow link might be useful for further debugging
# https://stackoverflow.com/questions/66841759/im-trying-to-send-an-email-from-django-using-gmail-smtp


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/images/'

# this is not a custom variable, so use the exact variable name
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# os.path.join(BASE_DIR, 'static')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

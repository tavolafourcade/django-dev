from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'ProyectoCoder.wsgi.local.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3')
,
    }
}

AUTH_PASSWORD_VALIDATORS = [

]
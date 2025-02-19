import os

from .defaults import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    'csmb-housewars.c4patino.com',
    'collegiate-housewars-02810c3f29dc.herokuapp.com',
]

CSRF_TRUSTED_ORIGINS = [
    'http://collegiate-housewars-02810c3f29dc.herokuapp.com/'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '3306'
    }
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

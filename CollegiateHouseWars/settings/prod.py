import os

from .defaults import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '45.79.52.230',
    'housewars.c4thebomb101.com',
    'collegiate-housewars.herokuapp.com',
    'collegiate-housewars.up.railway.app'
]

CSRF_TRUSTED_ORIGINS = [
    'https://housewars.c4thebomb101.com',
    'https://collegiate-housewars.herokuapp.com',
    'https://collegiate-housewars.up.railway.app'
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'housewars',
        'USER': os.environ.get('DATABASE_USERNAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '3306'
    }
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

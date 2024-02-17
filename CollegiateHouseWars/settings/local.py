from .defaults import *

SECRET_KEY = '*9r50c74r58p#*tnfpadsw*cp&$(^sj585w1u@!y9*eowmwl1*'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

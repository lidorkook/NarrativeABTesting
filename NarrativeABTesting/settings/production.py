from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'narrativeabtesting',
        'USER': 'narrativeabtesting',
        'PASSWORD': 'narrativeabtesting',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 60
    }
}

CORS_ORIGIN_ALLOW_ALL = True
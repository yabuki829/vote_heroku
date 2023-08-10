from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vote',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '3306',
    }
}
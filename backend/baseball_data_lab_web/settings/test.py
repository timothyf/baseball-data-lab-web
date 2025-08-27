from .base import *  # noqa

DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '3121018Fisher',
        'HOST': 'db.tigrhjeznfdtpjfgwane.supabase.co',
        'PORT': 5432,
    }
}

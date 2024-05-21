# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'money_v1',
        'USER': 'money',
        'PASSWORD': 'neymo',
        'HOST': '10.0.0.2',
        'PORT': 5432,
    }
}

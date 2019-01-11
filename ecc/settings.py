import os
import environ

env = environ.Env(
    DEBUG=(bool, False),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_USE_SSL=(bool, False),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'debug_toolbar',
    'model_utils',
    'easy_thumbnails',
    'filer',
    'ordered_model',
    'django_tabler',
    'django_extensions',

    'control',
    'magicauth',
    'user_profiles',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ecc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {'default': env.db()}

SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER',)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')


DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
MAGICAUTH_FROM_EMAIL = DEFAULT_FROM_EMAIL

MAGICAUTH_TOKEN_DURATION = 15 * 60

LOGIN_REDIRECT_URL = 'questionnaire-list'
LOGIN_URL = 'login'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Collect static won't work if you haven't configured this
# django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set
#  the STATIC_ROOT setting to a filesystem path.
DEFAULT_STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = env('STATIC_ROOT', default=DEFAULT_STATIC_ROOT)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Want forever-cacheable files and compression support?
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = env('MEDIA_ROOT', default=DEFAULT_MEDIA_ROOT)


SENDFILE_BACKEND = env('SENDFILE_BACKEND', default='sendfile.backends.development')
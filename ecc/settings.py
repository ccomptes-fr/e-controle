import os
import environ
import sys

env = environ.Env(
    DEBUG=(bool, False),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_USE_SSL=(bool, False),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# To secure access to files/dir, only the user used by the application can rw the files/dir.
CHOWN_MASK=0o700
# https://docs.djangoproject.com/en/3.2/ref/settings/#file-upload-directory-permissions
FILE_UPLOAD_DIRECTORY_PERMISSIONS=CHOWN_MASK
FILE_UPLOAD_PERMISSIONS=CHOWN_MASK

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

SHOW_DEBUG_TOOLBAR = env("SHOW_DEBUG_TOOLBAR", default=DEBUG)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda r: SHOW_DEBUG_TOOLBAR,
    "SHOW_COLLAPSED": True,
}

# https://docs.djangoproject.com/fr/3.2/topics/cache/#database-caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "webdav_cache",
    }
}

# Application definition

INSTALLED_APPS = [
    "admin_confirm",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third-party apps
    "debug_toolbar",
    "model_utils",
    "ordered_model",
    "django_extensions",
    "actstream",
    "rest_framework",
    "celery",
    "django_celery_beat",
    "django_cleanup.apps.CleanupConfig",
    "ckeditor",
    "django_filters",
    "django_admin",
    "email_obfuscator",
    "django_softdelete",
    # Project's apps
    "backoffice",
    "config",
    "control",
    "demo",
    "editor",
    "faq",
    "magicauth",
    "reporting",
    "user_profiles",
    "utils",
    "adauth",
    "session",
    "soft_deletion",
    "tos",
    "logs",
    "parametres",
    "alerte",
    # Central app - loaded last
    "ecc",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    #"csp.middleware.CSPMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "tos.middleware.WelcomeMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecc.urls"

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "ecc.context_processors.current_site",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
            ],
        },
    },
]

WSGI_APPLICATION = "ecc.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {"default": env.db()}

SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# HTTP Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
FEATURE_POLICY = {
    "geolocation": "none",
    "autoplay": [
        "self",
    ],
    "accelerometer": "none",
    "camera": "none",
    "gyroscope": "none",
    "magnetometer": "none",
    "microphone": "none",
    "payment": "none",
    "usb": "none",
}
# Strict-Transport-Security
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE: We have to use Lax and not Strict, otherwise login is broken when you login
# by clicking the magic link from gmail, orange mail, or other mail website with specific
# referer-policy.
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SAMESITE: We have to use Lax and not Strict, otherwise CRSF is broken when you
# login by clicking the magic link from gmail, orange mail, or other mail website with specific
# referer-policy.
SESSION_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 30
# Content-Security-Policy
CSP_DEFAULT_SRC = env(
    "CSP_DEFAULT_SRC", default=("'self'", "https://webanalytics.ccomptes.fr")
)
CSP_STYLE_SRC = env("CSP_STYLE_SRC", default=("'self'", "'unsafe-inline'"))
CSP_SCRIPT_SRC = env(
    "CSP_SCRIPT_SRC",
    default=(
        "'self'",
        "'unsafe-eval'",
        "'unsafe-inline'",
        "https://webanalytics.ccomptes.fr",    ),
)

if DEBUG:
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False

# Email
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_TIMEOUT = env("EMAIL_TIMEOUT", default=3)

EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_USE_SSL = env("EMAIL_USE_SSL")

# Time we wait in between emails, to space them out and avoid going over our allowed email quota
EMAIL_SPACING_TIME_MILLIS = env("EMAIL_SPACING_TIME_MILLIS", default=10000)

# The user will get a warning when trying to add an inspector whose email doesn't end with EXPECTED_INSPECTOR_EMAIL_ENDINGS
EXPECTED_INSPECTOR_EMAIL_ENDINGS = env("EXPECTED_INSPECTOR_EMAIL_ENDINGS", default="")

SEND_EMAIL_WHEN_USER_ADDED = env("SEND_EMAIL_WHEN_USER_ADDED", default=False)
SEND_EMAIL_WHEN_USER_REMOVED = env("SEND_EMAIL_WHEN_USER_REMOVED", default=False)

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SUPPORT_TEAM_EMAIL = env("SUPPORT_TEAM_EMAIL", default="support@e-controle.fr")

MAGICAUTH_FROM_EMAIL = DEFAULT_FROM_EMAIL
MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME = "control-detail"
MAGICAUTH_EMAIL_SUBJECT = "Connexion e.controle"
MAGICAUTH_EMAIL_HTML_TEMPLATE = "login/email.html"
MAGICAUTH_EMAIL_TEXT_TEMPLATE = "login/email.txt"
MAGICAUTH_LOGIN_VIEW_TEMPLATE = "login/login.html"
MAGICAUTH_EMAIL_SENT_VIEW_TEMPLATE = "login/email_sent.html"
MAGICAUTH_WAIT_VIEW_TEMPLATE = "login/wait.html"
MAGICAUTH_TOKEN_DURATION_SECONDS = env("MAGICAUTH_TOKEN_DURATION_SECONDS", default=300)

LOGIN_URL = "login"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# A trick for DRF that does not seems to know about the locale
import locale

try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except locale.Error as e:
    pass  # setlocale can crash, for instance when running on Heroku.

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

ADMIN_URL = env("ADMIN_URL", default="admin/")
# URL of e-controle in questionnaire
QUESTIONNAIRE_SITE_URL = env("QUESTIONNAIRE_SITE_URL", default="")

# Exclude incoming file if its mime type contains any of the following text
UPLOAD_FILE_MIME_TYPE_BLACKLIST = env(
    "UPLOAD_FILE_MIME_TYPE_BLACKLIST", default=("exe", "msi", "script")
)

UPLOAD_FILE_EXTENSION_BLACKLIST = env(
    "UPLOAD_FILE_EXTENSION_BLACKLIST", default=(".exe", ".dll")
)

UPLOAD_FILE_MAX_SIZE_MB = env("UPLOAD_FILE_MAX_SIZE_MB", default=256)

MAX_FILENAME_LENGTH = env("MAX_FILENAME_LENGTH", default=150)

STATIC_URL = "/static/"

# Collect static won't work if you haven't configured this
# django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set
#  the STATIC_ROOT setting to a filesystem path.
DEFAULT_STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_ROOT = env("STATIC_ROOT", default=DEFAULT_STATIC_ROOT)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # NPM modules that we need to link in <script> tags directly : add them to static files.
    os.path.join(BASE_DIR, "node_modules", "bootstrap", "dist", "js"),
    os.path.join(BASE_DIR, "node_modules", "jquery", "dist"),
]

# Want forever-cacheable files and compression support?
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_ROOT = env("MEDIA_ROOT", default=DEFAULT_MEDIA_ROOT)

SENDFILE_BACKEND = env("SENDFILE_BACKEND", default="sendfile.backends.simple")

PIWIK_TRACKER_BASE_URL = env("PIWIK_TRACKER_BASE_URL", default=None)
PIWIK_SITE_ID = env("PIWIK_SITE_ID", default=None)

SETTINGS_EXPORT = [
    "PIWIK_SITE_ID",
    "PIWIK_TRACKER_BASE_URL",
    "SESSION_EXPIRE_SECONDS",
    "SUPPORT_TEAM_EMAIL",
    "WEBDAV_URL",
    "DEBUG",
    "SAVE_IP_ADDRESS",
    "ENV_NAME",
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
HTTP_AUTHORIZATION = env("HTTP_AUTHORIZATION", default=None)

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    }
}

# LDAP configuration for WEBDAV configuration

LDAP_SERVER = env("LDAP_SERVER", default=None)
LDAP_USER = env("LDAP_USER", default=None)
LDAP_DOMAIN = env("LDAP_DOMAIN", default=None)
LDAP_PASSWORD = env("LDAP_PASSWORD", default=None)
LDAP_DC = env("LDAP_DC", default=None)
TITLE_TO_COME_IN = env("TITLE_TO_COME_IN", default="").split(",")
MAGICAUTH_EMAIL_UNKNOWN_CALLBACK = "adauth.auth.active_directory_auth"
WEBDAV_URL = env("WEBDAV_URL", default="https://e-controle-webdav.ccomptes.fr")
# timeout in seconds, cache the can_user_access_realm corresponding to the samaccount
WEBDAV_CACHE_TIMEOUT = env("WEBDAV_CACHE_TIMEOUT", default=30 * 60)

DEMO_INSPECTOR_USERNAME = env("DEMO_INSPECTOR_USERNAME", default=None)
DEMO_AUDITED_USERNAME = env("DEMO_AUDITED_USERNAME", default=None)
ALLOW_DEMO_LOGIN = env("ALLOW_DEMO_LOGIN", default=False)

# Session management
SESSION_EXPIRE_SECONDS = env("SESSION_EXPIRE_SECONDS", default=24 * 60 * 60)
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# Ip adress
SAVE_IP_ADDRESS = env("SAVE_IP_ADDRESS", default=True)

# Environnement name
ENV_NAME = env("ENV_NAME", default="")

# Logging config for production
# we must check filename not none to run 2 separates logs files
# 1 file for econtrole and 1 file for econtrole-webdav
# https://mattsegal.dev/django-gunicorn-nginx-logging.html
# https://mattsegal.dev/file-logging-django.html
#  APP_NAME come from gunicorn config
FILENAME = env("APP_NAME", default=None)
if not DEBUG and FILENAME:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": "ERROR", "handlers": ["file"]},
        "formatters": {
            "verbose": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
        },
        "handlers": {
            "file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": f"/var/log/{FILENAME}.log",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {"handlers": ["file"], "level": "ERROR", "propagate": True},
        },
    }
else:
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }

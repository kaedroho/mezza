"""
Django settings for mezza project.

Generated by 'npm create django-bridge' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
import sentry_sdk

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Basic Django settings

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DJANGO_DEBUG", "false") == "true"
BASE_URL = os.environ["BASE_URL"]
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", urlparse(BASE_URL).hostname
).split(",")
CSRF_TRUSTED_ORIGINS_STR = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS") or BASE_URL
if CSRF_TRUSTED_ORIGINS_STR:
    CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS_STR.split(",")
else:
    CSRF_TRUSTED_ORIGINS = []
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition

INSTALLED_APPS = [
    "mezza.files",
    "mezza.workspaces",
    "mezza.auth",
    "mezza",
    "django_bridge",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_bridge.middleware.DjangoBridgeMiddleware",
]

ROOT_URLCONF = "mezza.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mezza.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(default="sqlite:///db.sqlite3")}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = os.environ.get("DJANGO_STATIC_URL", "static/")

if os.environ.get("VITE_BUNDLE_DIR"):
    STATICFILES_DIRS = [os.environ["VITE_BUNDLE_DIR"]]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

if "BACKBLAZE_BUCKET" in os.environ:
    BACKBLAZE_REGION = os.environ["BACKBLAZE_REGION"]
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.environ["BACKBLAZE_BUCKET"],
            "access_key": os.environ["BACKBLAZE_KEY_ID"],
            "secret_key": os.environ["BACKBLAZE_APPLICATION_KEY"],
            "region_name": BACKBLAZE_REGION,
            "endpoint_url": f"https://s3.{BACKBLAZE_REGION}.backblazeb2.com",
        },
    }

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth

AUTH_USER_MODEL = "mezzaauth.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "login_redirect"

# Logging
# Log all warnings to console

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

# Sentry

if "SENTRY_DSN" in os.environ:
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

# Django Bridge settings

DJANGO_BRIDGE = {
    "VITE_BUNDLE_DIR": os.environ.get("VITE_BUNDLE_DIR"),
    "VITE_DEVSERVER_URL": os.environ.get("VITE_SERVER_ORIGIN"),
    "CONTEXT_PROVIDERS": {
        "csrf_token": "django.middleware.csrf.get_token",
        "urls": "mezza.context_providers.urls",
        "workspaces": "mezza.context_providers.workspaces",
    },
}

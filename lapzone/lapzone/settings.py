import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv("SECRET_KEY"))

DEBUG = bool(os.getenv("DEBUG"))

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lapzone.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "lapzone.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "PORT": int(os.getenv("DB_PORT")),
        "HOST": str(os.getenv("DB_HOST")),
        "NAME": str(os.getenv("DB_NAME")),
        "USER": str(os.getenv("DB_USER")),
        "PASSWORD": str(os.getenv("DB_PASSWORD")),
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

STATIC_URL = "static/"
STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

SITE_ID = 1

EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST = str(os.getenv("EMAIL_HOST_USER"))
EMAIL_USE_TLS = bool(os.getenv("EMAIL_USE_TLS"))
EMAIL_USE_SSL = bool(os.getenv("EMAIL_USE_SSL"))
EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))
EMAIL_BACKEND = str(os.getenv("EMAIL_HOST_USER"))

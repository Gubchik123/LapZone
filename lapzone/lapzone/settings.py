import logging
import os
import sys
from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv("SECRET_KEY"))

DEBUG = True

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third-party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "ckeditor",
    "ckeditor_uploader",
    "snowpenguin.django.recaptcha3",
    # My apps
    "shop.apps.ShopConfig",
    "cart.apps.CartConfig",
    "order.apps.OrderConfig",
    "customer.apps.CustomerConfig",
    "mailing.apps.MailingConfig",
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
                # Django context processors
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # My custom context processors
                "cart.context_processors.cart",
                "mailing.context_processors.mailing_form",
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

TIME_ZONE = "Europe/Kiev"

USE_I18N = False

USE_TZ = True

STATIC_URL = "static/"
STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[LapZone] "
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60 * 10  # 10 minutes
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_MIN_LENGTH = 2

SOCIALACCOUNT_PROVIDERS = {  # OAuth providers
    "google": {
        "APP": {
            "client_id": str(os.getenv("GOOGLE_OAUTH_CLIENT_ID")),
            "secret": str(os.getenv("GOOGLE_OAUTH_SECRET")),
            "key": "",
        }
    },
    "github": {
        "APP": {
            "client_id": str(os.getenv("GITHUB_OAUTH_CLIENT_ID")),
            "secret": str(os.getenv("GITHUB_OAUTH_SECRET")),
            "key": "",
        }
    },
}
SOCIALACCOUNT_LOGIN_ON_GET = True

LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = reverse_lazy("account_login")
LOGIN_REDIRECT_URL = reverse_lazy("customer:detail")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

MESSAGE_TAGS = {messages.INFO: "primary", messages.ERROR: "danger"}

SITE_ID = 1

EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST = str(os.getenv("EMAIL_HOST"))
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))
EMAIL_BACKEND = str(os.getenv("EMAIL_BACKEND"))

RECAPTCHA_PUBLIC_KEY = str(os.getenv("RECAPTCHA_PUBLIC_KEY"))
RECAPTCHA_PRIVATE_KEY = str(os.getenv("RECAPTCHA_PRIVATE_KEY"))
RECAPTCHA_DEFAULT_ACTION = "generic"
RECAPTCHA_SCORE_THRESHOLD = 0.5

CART_SESSION_ID = "cart"

ERROR_MESSAGE = "There was an error; please try again later."

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{name}: [{asctime}] {levelname} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "general.views": {
            "level": "ERROR",
            "propagate": False,
            "handlers": ["console", "mail_admins"],
        },
    },
}

if TESTING:
    logging.disable(logging.CRITICAL)

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": [
                    "Preview",
                    "Print",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "PasteText",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {
                "name": "editing",
                "items": ["Find", "Replace"],
            },
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                ],
            },
            "/",
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Youtube",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe",
                ],
            },
            "/",
            {"name": "styles", "items": ["Format", "Font", "FontSize"]},
            {"name": "tools", "items": ["Maximize"]},
        ],
        "toolbar": "YourCustomToolbarConfig",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # extra plugins
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
                "youtube",
            ]
        ),
    }
}

if DEBUG and not TESTING:
    import mimetypes


    mimetypes.add_type("application/javascript", ".js", True)

    INSTALLED_APPS.insert(15, "debug_toolbar")

    MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")

    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

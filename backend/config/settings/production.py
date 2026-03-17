import os

import sentry_sdk
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401, F403

DEBUG = False

# WhiteNoise for static files
MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,  # noqa: F405
    "whitenoise.middleware.WhiteNoiseMiddleware",
)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# SECRET_KEY guard — reject the insecure default from base.py
if SECRET_KEY == "django-insecure-change-me-in-production":  # noqa: F405
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be set to a unique, random value in production."
    )

# ALLOWED_HOSTS — filter empty strings, require at least one
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS environment variable must be set (comma-separated hostnames)."
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "pystarter"),
        "USER": os.environ.get("DB_USER", "pystarter"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# CORS — filter empty strings, require at least one
CORS_ALLOWED_ORIGINS = [
    o for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
if not CORS_ALLOWED_ORIGINS:
    raise ImproperlyConfigured(
        "CORS_ALLOWED_ORIGINS environment variable must be set (comma-separated origins)."
    )

# SSL / Cookie security — disable via DISABLE_SSL=true for local Docker without HTTPS
_ssl_enabled = os.environ.get("DISABLE_SSL", "").lower() not in ("true", "1", "yes")
SECURE_SSL_REDIRECT = _ssl_enabled
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = _ssl_enabled
CSRF_COOKIE_SECURE = _ssl_enabled

# HSTS — conservative settings for first release
SECURE_HSTS_SECONDS = 3600  # 1 hour — safe to test, easy to roll back
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False  # Do NOT enable preload on first release — it's irreversible
SECURE_CONTENT_TYPE_NOSNIFF = True

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

# Sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.1)

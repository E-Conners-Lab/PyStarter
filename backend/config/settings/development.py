from .base import *  # noqa: F401, F403

DEBUG = os.environ.get("DJANGO_DEBUG", "").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
SIMPLE_JWT = {**SIMPLE_JWT, "AUTH_COOKIE_SECURE": False}  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:5174"]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Recovery emails require explicitly configured SMTP; never print reset tokens.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

# Disable throttling in development (prevents test flakiness)
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}

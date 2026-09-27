"""Isolated browser-test settings; never used by the packaged application."""
from .development import *  # noqa: F403

# The suite registers many independent learners from one browser host.
# Production/auth regression tests keep the real 10/minute boundary.
AUTH_RATE_LIMIT = 10000
CSRF_TRUSTED_ORIGINS = ['http://localhost:5187']
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

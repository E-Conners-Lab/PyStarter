"""Database-backed sliding windows and password-guess lockouts."""
from datetime import timedelta
import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import salted_hmac
from rest_framework.exceptions import Throttled
from rest_framework.throttling import BaseThrottle

from .models import AuthenticationAttempt

logger = logging.getLogger(__name__)
MAX_FAILURES = 5
LOCKOUT_SECONDS = 15 * 60


def identity_key(kind, value):
    return salted_hmac("pystarter.auth." + kind, value, algorithm="sha256").hexdigest()


class AuthenticationThrottle(BaseThrottle):
    def allow_request(self, request, view):
        now = timezone.now()
        window = getattr(settings, "AUTH_RATE_WINDOW_SECONDS", 60)
        limit = getattr(settings, "AUTH_RATE_LIMIT", 10)
        # Bound retained state; no caller-provided identity survives as plaintext.
        AuthenticationAttempt.objects.filter(updated_at__lt=now - timedelta(days=1)).delete()
        key = identity_key("ip", request.META.get("REMOTE_ADDR", "unknown"))
        with transaction.atomic():
            record, _ = AuthenticationAttempt.objects.select_for_update().get_or_create(identity=key)
            recent = [stamp for stamp in record.request_times if stamp > now.timestamp() - window]
            if len(recent) >= limit:
                return False
            AuthenticationAttempt.objects.filter(pk=key).update(
                request_times=[*recent, now.timestamp()], updated_at=now,
            )
        return True

    def wait(self):
        return getattr(settings, "AUTH_RATE_WINDOW_SECONDS", 60)


def authenticate_with_lockout(request, username, password):
    now = timezone.now()
    key = identity_key("username", username)
    with transaction.atomic():
        record, _ = AuthenticationAttempt.objects.select_for_update().get_or_create(identity=key)
        if record.locked_until and record.locked_until > now:
            raise Throttled(wait=LOCKOUT_SECONDS)
        user = authenticate(request, username=username, password=password)
        previous = record.failures if record.updated_at > now - timedelta(seconds=LOCKOUT_SECONDS) else 0
        failures = previous + 1 if user is None else 0
        lock_until = now + timedelta(seconds=LOCKOUT_SECONDS) if failures >= MAX_FAILURES else None
        AuthenticationAttempt.objects.filter(pk=key).update(
            failures=failures, locked_until=lock_until, updated_at=now,
        )
    if user is None:
        logger.info("audit: action=login_failed")
    return user

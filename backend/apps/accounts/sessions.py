"""Cookie and token lifecycle shared by login, refresh, logout and reset."""
from django.conf import settings
from django.middleware.csrf import get_token, rotate_token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

ACCOUNTS_PATH = "/api/v1/accounts/"


def issue_refresh(user):
    refresh = RefreshToken.for_user(user)
    refresh["session_jti"] = refresh["jti"]
    return refresh


def set_auth_cookies(response, refresh, request=None):
    jwt_settings = settings.SIMPLE_JWT
    for name, token, lifetime, path in (
        ("access_token", refresh.access_token, "ACCESS_TOKEN_LIFETIME", "/"),
        ("refresh_token", refresh, "REFRESH_TOKEN_LIFETIME", ACCOUNTS_PATH),
    ):
        response.set_cookie(
            name, str(token), httponly=True, samesite="Strict",
            secure=jwt_settings.get("AUTH_COOKIE_SECURE", True),
            max_age=int(jwt_settings[lifetime].total_seconds()), path=path,
        )
    if request is not None:
        rotate_token(request)
        response["X-CSRFToken"] = get_token(request)
    response["Cache-Control"] = "no-store"


def clear_auth_cookies(response):
    for name, path in (("access_token", "/"), ("refresh_token", ACCOUNTS_PATH)):
        response.delete_cookie(name, path=path, samesite="Strict")
    response["Cache-Control"] = "no-store"


def revoke_session_cookies(request):
    raw_refresh = request.COOKIES.get("refresh_token")
    if raw_refresh:
        try:
            RefreshToken(raw_refresh).blacklist()
        except TokenError:
            pass  # Expired or already-revoked refresh tokens cannot be reused.
    raw_access = request.COOKIES.get("access_token")
    if raw_access:
        try:
            access = AccessToken(raw_access)
        except TokenError:
            return  # Invalid access tokens cannot authenticate.
        outstanding = OutstandingToken.objects.filter(jti=access.get("session_jti")).first()
        if outstanding:
            BlacklistedToken.objects.get_or_create(token=outstanding)

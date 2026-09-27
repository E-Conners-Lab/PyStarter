from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def enforce_csrf(request):
    """DRF views are middleware-exempt, so enforce CSRF explicitly."""
    if request.method not in SAFE_METHODS:
        if request.META.get("HTTP_SEC_FETCH_SITE") == "cross-site":
            raise PermissionDenied("Cross-site requests are not allowed.")
        SessionAuthentication().enforce_csrf(request)


class RequireCSRF(BasePermission):
    def has_permission(self, request, view):
        enforce_csrf(request)
        return True


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return super().authenticate(request)
        enforce_csrf(request)
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        session_jti = validated_token.get("session_jti")
        if not session_jti or BlacklistedToken.objects.filter(token__jti=session_jti).exists():
            raise AuthenticationFailed("Session has expired. Please sign in again.")
        return user

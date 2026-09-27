import logging
from smtplib import SMTPException

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.middleware.csrf import get_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError

from apps.common.authentication import CookieJWTAuthentication, RequireCSRF
from .sessions import clear_auth_cookies, issue_refresh, revoke_session_cookies, set_auth_cookies
from .login_security import AuthenticationThrottle, authenticate_with_lockout

from apps.common.throttles import PasswordResetThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from apps.curriculum.models import Exercise, Module

from .serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = [RequireCSRF]
    throttle_classes = [AuthenticationThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Unlock the first module for the new user
        first_module = Module.objects.filter(is_published=True).order_by("order").first()
        if first_module:
            from apps.accounts.models import UserModuleProgress

            UserModuleProgress.objects.get_or_create(
                user=user,
                module=first_module,
                defaults={"is_unlocked": True},
            )

        refresh = issue_refresh(user)
        response = Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )
        set_auth_cookies(response, refresh, request)
        logger.info(
            "audit: action=register user_id=%s", user.pk,
        )
        return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([RequireCSRF])
@throttle_classes([AuthenticationThrottle])
def login_view(request):
    """Authenticate user and set JWT cookies."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate_with_lockout(request, **serializer.validated_data)
    if user is None:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    refresh = issue_refresh(user)
    response = Response({"user": UserSerializer(user).data})
    set_auth_cookies(response, refresh, request)
    logger.info(
        "audit: action=login user_id=%s", user.pk,
    )
    return response


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def progress_summary(request):
    user = request.user
    modules_total = Module.objects.filter(is_published=True).count()
    modules_completed = user.module_progress.filter(is_completed=True).count()
    exercises_total = Exercise.objects.filter(
        is_published=True, lesson__is_published=True, lesson__module__is_published=True
    ).count()
    exercises_completed = user.exercise_progress.filter(is_completed=True).count()

    return Response(
        {
            "total_xp": user.total_xp,
            "current_belt": user.current_belt,
            "current_belt_display": user.current_belt_display,
            "next_belt_xp": user.next_belt_xp,
            "modules_completed": modules_completed,
            "modules_total": modules_total,
            "exercises_completed": exercises_completed,
            "exercises_total": exercises_total,
            "current_streak": user.current_streak,
            "longest_streak": user.longest_streak,
        }
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def csrf_token(request):
    response = Response({"csrfToken": get_token(request)})
    # Clear the old narrow-path refresh cookie before the browser signs in.
    # A separate bootstrap response allows Set-Cookie for the legacy path
    # without overwriting the current same-name cookie in Django SimpleCookie.
    response.delete_cookie("refresh_token", path="/api/v1/accounts/token/refresh/", samesite="Strict")
    response["Cache-Control"] = "no-store"
    return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([RequireCSRF])
def logout_view(request):
    """Revoke the session even if its access token has expired."""
    revoke_session_cookies(request)
    response = Response({"status": "logged out"})
    clear_auth_cookies(response)
    logger.info("audit: action=logout")
    return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([RequireCSRF])
@throttle_classes([AuthenticationThrottle])
def token_refresh(request):
    """Rotate a refresh cookie without authenticating an expired access cookie."""
    raw_token = request.COOKIES.get("refresh_token")
    try:
        with transaction.atomic():
            refresh = RefreshToken(raw_token) if raw_token else None
            if refresh is None:
                raise TokenError("Missing refresh token")
            user = CookieJWTAuthentication().get_user(refresh)
            # Serialize refreshes so the same token cannot produce two successors.
            user = User.objects.select_for_update().get(pk=user.pk)
            CookieJWTAuthentication().get_user(refresh)
            refresh.check_blacklist()
            refresh.blacklist()
            response = Response({"status": "refreshed"})
            set_auth_cookies(response, issue_refresh(user))
            return response
    except (TokenError, AuthenticationFailed, User.DoesNotExist):
        response = Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        clear_auth_cookies(response)
        return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([RequireCSRF])
@throttle_classes([AuthenticationThrottle, PasswordResetThrottle])
def password_reset_request(request):
    """Send a password reset email. Always returns 200 (anti-enumeration)."""
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    response = Response({"status": "If an account with that email exists, a reset link has been sent."})
    if settings.EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend" and not settings.EMAIL_HOST.strip():
        logger.warning("Password recovery unavailable: SMTP host is not configured.")
        return response

    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}"
        send_mail(
            subject="PyStarter — Password Reset",
            message=f"Click the link to reset your password:\n\n{reset_link}\n\nIf you did not request this, ignore this email.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass  # Anti-enumeration: don't reveal if email exists
    except (SMTPException, OSError):
        logger.warning("Password recovery delivery failed; check SMTP configuration.")

    logger.info(
        "audit: action=password_reset_request",
    )
    return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([RequireCSRF])
@throttle_classes([AuthenticationThrottle, PasswordResetThrottle])
def password_reset_confirm(request):
    """Reset password using uid and token from the email link."""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        uid = force_str(urlsafe_base64_decode(serializer.validated_data["uid"]))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {"error": "Invalid reset link."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not default_token_generator.check_token(user, serializer.validated_data["token"]):
        return Response(
            {"error": "Invalid or expired reset link."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        validate_password(serializer.validated_data["new_password"], user)
    except DjangoValidationError as e:
        return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data["new_password"])
    user.save()
    logger.info(
        "audit: action=password_reset_confirm user_id=%s", user.pk,
    )
    response = Response({"status": "Password has been reset successfully."})
    clear_auth_cookies(response)
    return response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([RequireCSRF])
def leaderboard(request):
    users = User.objects.order_by("-total_xp")[:20]
    data = [
        {
            "username": u.username,
            "total_xp": u.total_xp,
            "current_belt": u.current_belt,
            "current_belt_display": u.current_belt_display,
        }
        for u in users
    ]
    return Response(data)

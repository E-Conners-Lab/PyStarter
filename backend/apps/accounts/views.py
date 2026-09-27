import logging

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from apps.common.throttles import PasswordResetThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from apps.curriculum.models import Exercise, Module

from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)

User = get_user_model()


def _set_auth_cookies(response, refresh):
    """Set access and refresh token cookies on a response."""
    jwt_settings = settings.SIMPLE_JWT
    response.set_cookie(
        "access_token",
        str(refresh.access_token),
        httponly=True,
        samesite="Lax",
        secure=jwt_settings.get("AUTH_COOKIE_SECURE", False),
        max_age=int(jwt_settings["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        str(refresh),
        httponly=True,
        samesite="Lax",
        secure=jwt_settings.get("AUTH_COOKIE_SECURE", False),
        max_age=int(jwt_settings["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path="/api/v1/accounts/token/refresh/",
    )


def _clear_auth_cookies(response):
    """Delete auth cookies from a response."""
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/api/v1/accounts/token/refresh/")


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

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

        refresh = RefreshToken.for_user(user)
        response = Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )
        _set_auth_cookies(response, refresh)
        logger.info(
            "audit: action=register user=%s ip=%s",
            user.username,
            request.META.get("REMOTE_ADDR"),
        )
        return response


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Authenticate user and set JWT cookies."""
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    refresh = RefreshToken.for_user(user)
    response = Response({"user": UserSerializer(user).data})
    _set_auth_cookies(response, refresh)
    logger.info(
        "audit: action=login user=%s ip=%s",
        user.username,
        request.META.get("REMOTE_ADDR"),
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


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Blacklist the current refresh token and clear cookies."""
    refresh_token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
    response = Response({"status": "logged out"})
    _clear_auth_cookies(response)
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            logger.warning("Failed to blacklist refresh token during logout")
            _clear_auth_cookies(response)
            response.data = {
                "error": "Logout may not have completed fully. Your session will expire automatically."
            }
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return response
    logger.info(
        "audit: action=logout user=%s ip=%s",
        request.user.username,
        request.META.get("REMOTE_ADDR"),
    )
    return response


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def token_refresh(request):
    """Refresh access token using the refresh token cookie."""
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return Response({"error": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        refresh = RefreshToken(refresh_token)
        response = Response({"status": "refreshed"})
        jwt_settings = settings.SIMPLE_JWT
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            samesite="Lax",
            secure=jwt_settings.get("AUTH_COOKIE_SECURE", False),
            max_age=int(jwt_settings["ACCESS_TOKEN_LIFETIME"].total_seconds()),
            path="/",
        )
        if jwt_settings.get("ROTATE_REFRESH_TOKENS", False):
            refresh.blacklist()
            user = User.objects.get(pk=refresh.access_token["user_id"])
            new_refresh = RefreshToken.for_user(user)
            response.set_cookie(
                "refresh_token",
                str(new_refresh),
                httponly=True,
                samesite="Lax",
                secure=jwt_settings.get("AUTH_COOKIE_SECURE", False),
                max_age=int(jwt_settings["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                path="/api/v1/accounts/token/refresh/",
            )
        return response
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([PasswordResetThrottle])
def password_reset_request(request):
    """Send a password reset email. Always returns 200 (anti-enumeration)."""
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]

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

    logger.info(
        "audit: action=password_reset_request email=%s ip=%s",
        email,
        request.META.get("REMOTE_ADDR"),
    )
    return Response({"status": "If an account with that email exists, a reset link has been sent."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([PasswordResetThrottle])
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
        "audit: action=password_reset_confirm user=%s ip=%s",
        user.username,
        request.META.get("REMOTE_ADDR"),
    )
    return Response({"status": "Password has been reset successfully."})


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
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

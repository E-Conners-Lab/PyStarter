from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
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

User = get_user_model()


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
        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


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
    """Blacklist the current refresh token."""
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "Refresh token is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        pass  # Token may already be blacklisted or invalid
    return Response({"status": "logged out"})


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

    return Response({"status": "If an account with that email exists, a reset link has been sent."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
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

    user.set_password(serializer.validated_data["new_password"])
    user.save()
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

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.curriculum.models import Exercise, Module

from .serializers import RegisterSerializer, UserSerializer

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

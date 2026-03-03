from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.accounts.models import UserExerciseProgress, UserLessonProgress, UserModuleProgress

from .models import Exercise, Hint, Lesson, Module
from .serializers import (
    ExerciseDetailSerializer,
    HintSerializer,
    LessonDetailSerializer,
    ModuleDetailSerializer,
    ModuleListSerializer,
)


class ModuleListView(ListAPIView):
    serializer_class = ModuleListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Module.objects.filter(is_published=True).prefetch_related(
            "lessons", "lessons__exercises", "user_progress"
        )


class ModuleDetailView(RetrieveAPIView):
    serializer_class = ModuleDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Module.objects.filter(is_published=True).prefetch_related(
            "lessons", "user_progress"
        )


class LessonDetailView(RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        module_slug = self.kwargs["module_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        return Lesson.objects.select_related("module").prefetch_related(
            "exercises", "exercises__user_progress"
        ).get(
            module__slug=module_slug,
            slug=lesson_slug,
            is_published=True,
            module__is_published=True,
        )


class ExerciseDetailView(RetrieveAPIView):
    serializer_class = ExerciseDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        module_slug = self.kwargs["module_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        exercise_slug = self.kwargs["exercise_slug"]
        return Exercise.objects.select_related("lesson", "lesson__module").prefetch_related(
            "test_cases", "hints", "user_progress"
        ).get(
            lesson__module__slug=module_slug,
            lesson__slug=lesson_slug,
            slug=exercise_slug,
            is_published=True,
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def reveal_hint(request, exercise_id):
    """Reveal the next hint for an exercise."""
    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get user's exercise progress
    progress, _ = UserExerciseProgress.objects.get_or_create(
        user=request.user, exercise=exercise
    )

    # Find the next unrevealed hint
    next_level = progress.hints_used + 1
    try:
        hint = Hint.objects.get(exercise=exercise, level=next_level)
    except Hint.DoesNotExist:
        return Response({"error": "No more hints available"}, status=status.HTTP_404_NOT_FOUND)

    # Update hints used
    progress.hints_used = next_level
    progress.save(update_fields=["hints_used"])

    return Response(HintSerializer(hint).data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def revealed_hints(request, exercise_id):
    """Get all hints the user has already revealed for an exercise."""
    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    progress = UserExerciseProgress.objects.filter(
        user=request.user, exercise=exercise
    ).first()

    hints_used = progress.hints_used if progress else 0
    hints = Hint.objects.filter(exercise=exercise, level__lte=hints_used)
    return Response(HintSerializer(hints, many=True).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_lesson_complete(request, lesson_id):
    """Mark a concept/interactive lesson as completed (no exercise required)."""
    try:
        lesson = Lesson.objects.get(id=lesson_id, is_published=True)
    except Lesson.DoesNotExist:
        return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

    if lesson.lesson_type == "exercise":
        return Response(
            {"error": "Exercise lessons are completed by passing exercises."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save(update_fields=["is_completed", "completed_at"])

    _check_module_completion(request.user, lesson.module)

    return Response({"status": "completed"})


def _check_module_completion(user, module):
    """Check if all lessons/exercises in a module are done, and unlock the next module."""
    all_lessons = module.lessons.filter(is_published=True)
    all_completed = True

    for lesson in all_lessons:
        # Check lesson progress
        lesson_done = UserLessonProgress.objects.filter(
            user=user, lesson=lesson, is_completed=True
        ).exists()

        if not lesson_done:
            # For exercise lessons, check if all exercises are done
            if lesson.lesson_type == "exercise":
                exercises = lesson.exercises.filter(is_published=True)
                exercises_done = all(
                    UserExerciseProgress.objects.filter(
                        user=user, exercise=ex, is_completed=True
                    ).exists()
                    for ex in exercises
                )
                if exercises_done and exercises.exists():
                    # Auto-complete the lesson
                    UserLessonProgress.objects.update_or_create(
                        user=user,
                        lesson=lesson,
                        defaults={"is_completed": True, "completed_at": timezone.now()},
                    )
                else:
                    all_completed = False
            else:
                all_completed = False

    if all_completed:
        # Mark module as completed
        UserModuleProgress.objects.update_or_create(
            user=user,
            module=module,
            defaults={"is_completed": True, "completed_at": timezone.now()},
        )
        # Unlock the next module
        next_module = (
            Module.objects.filter(is_published=True, order__gt=module.order)
            .order_by("order")
            .first()
        )
        if next_module:
            UserModuleProgress.objects.get_or_create(
                user=user,
                module=next_module,
                defaults={"is_unlocked": True},
            )

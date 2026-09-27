from django.conf import settings
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from apps.common.throttles import AIRequestThrottle
from apps.curriculum.models import Exercise
from apps.submissions.models import Submission

from .prompts import (
    BEGINNER_HINT_SYSTEM,
    BEGINNER_HINT_USER,
    CODE_CRITIQUE_SYSTEM,
    CODE_CRITIQUE_USER,
    EXPLAIN_ERROR_SYSTEM,
    EXPLAIN_ERROR_USER,
)
from .providers import get_provider
from .input_boundary import TutorInputSerializer, UNTRUSTED_GUIDANCE, bounded_prompt

def _not_configured():
    return Response(
        {"error": "AI features are not configured."},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


def _validated_input(request):
    serializer = TutorInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def _has_passed(user, exercise):
    """Whether this user has a passing submission for this exercise.

    Critique embeds exercise.solution_code in the prompt, so an ungated endpoint
    is an answer-key disclosure surface: a caller who has not solved the exercise
    can steer the model into revealing it.
    """
    return Submission.objects.filter(user=user, exercise=exercise, status="passed", is_run_only=False).exists()


def _ai_is_configured():
    """Check if an AI provider is available."""
    key = getattr(settings, "ANTHROPIC_API_KEY", "")
    base_url = getattr(settings, "ANTHROPIC_BASE_URL", "")
    # Either a real API key or a local LLM base URL must be set
    return bool(key and key != "not-needed") or bool(base_url)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@throttle_classes([AIRequestThrottle])
def ai_hint(request, exercise_id):
    """Get an AI-generated hint for an exercise."""
    if not _ai_is_configured():
        return _not_configured()

    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True, lesson__is_published=True, lesson__module__is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    data = _validated_input(request)
    code, error = data["code"], data["error"]

    error_context = ""
    if error:
        error_context = f"They got this error:\n{error}"

    user_prompt = BEGINNER_HINT_USER.format(
        exercise_title=exercise.title,
        instructions=exercise.instructions,
        concepts=exercise.concepts,
        code=code,
        error_context=error_context,
    )

    provider = get_provider()
    hint = provider.generate(BEGINNER_HINT_SYSTEM + UNTRUSTED_GUIDANCE, bounded_prompt(user_prompt))
    return Response({"hint": hint})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@throttle_classes([AIRequestThrottle])
def ai_critique(request, exercise_id):
    """Get AI feedback on a successful submission."""
    if not _ai_is_configured():
        return _not_configured()

    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True, lesson__is_published=True, lesson__module__is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    if not _has_passed(request.user, exercise):
        return Response(
            {"error": "Solve the exercise first to get a critique."},
            status=status.HTTP_403_FORBIDDEN,
        )

    code = _validated_input(request)["code"]

    user_prompt = CODE_CRITIQUE_USER.format(
        exercise_title=exercise.title,
        instructions=exercise.instructions,
        code=code,
        solution_code="[omitted]",
    )

    provider = get_provider()
    feedback = provider.generate(CODE_CRITIQUE_SYSTEM + UNTRUSTED_GUIDANCE, bounded_prompt(user_prompt))
    return Response({"feedback": feedback})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@throttle_classes([AIRequestThrottle])
def explain_error(request, exercise_id):
    """Get a beginner-friendly explanation of an error."""
    if not _ai_is_configured():
        return _not_configured()

    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True, lesson__is_published=True, lesson__module__is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    data = _validated_input(request)
    code, error = data["code"], data["error"]

    if not error:
        return Response(
            {"error": "No error message provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    user_prompt = EXPLAIN_ERROR_USER.format(
        exercise_title=exercise.title,
        code=code,
        error=error,
    )

    provider = get_provider()
    explanation = provider.generate(EXPLAIN_ERROR_SYSTEM + UNTRUSTED_GUIDANCE, bounded_prompt(user_prompt))
    return Response({"explanation": explanation})

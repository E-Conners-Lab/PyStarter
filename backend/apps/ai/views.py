from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.curriculum.models import Exercise

from .prompts import (
    BEGINNER_HINT_SYSTEM,
    BEGINNER_HINT_USER,
    CODE_CRITIQUE_SYSTEM,
    CODE_CRITIQUE_USER,
    EXPLAIN_ERROR_SYSTEM,
    EXPLAIN_ERROR_USER,
)
from .providers import get_provider


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def ai_hint(request, exercise_id):
    """Get an AI-generated hint for an exercise."""
    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    code = request.data.get("code", "")
    error = request.data.get("error", "")

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
    hint = provider.generate(BEGINNER_HINT_SYSTEM, user_prompt)
    return Response({"hint": hint})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def ai_critique(request, exercise_id):
    """Get AI feedback on a successful submission."""
    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    code = request.data.get("code", "")

    user_prompt = CODE_CRITIQUE_USER.format(
        exercise_title=exercise.title,
        instructions=exercise.instructions,
        code=code,
        solution_code=exercise.solution_code or "Not available",
    )

    provider = get_provider()
    feedback = provider.generate(CODE_CRITIQUE_SYSTEM, user_prompt)
    return Response({"feedback": feedback})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def explain_error(request, exercise_id):
    """Get a beginner-friendly explanation of an error."""
    try:
        exercise = Exercise.objects.get(id=exercise_id, is_published=True)
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    code = request.data.get("code", "")
    error = request.data.get("error", "")

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
    explanation = provider.generate(EXPLAIN_ERROR_SYSTEM, user_prompt)
    return Response({"explanation": explanation})

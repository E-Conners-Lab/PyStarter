from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.models import UserExerciseProgress, UserLessonProgress
from apps.curriculum.models import Exercise, Hint
from apps.curriculum.views import _check_module_completion
from apps.executor.sandbox import compare_output, execute_code

from .models import Submission, TestCaseResult
from .serializers import SubmissionSerializer, SubmitCodeSerializer


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def sandbox_run(request):
    """Run code freely in the sandbox — no exercise or test cases needed."""
    serializer = SubmitCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data["code"]

    result = execute_code(code)
    return Response({
        "status": result["status"],
        "output": result.get("output", ""),
        "error": result.get("error", ""),
        "execution_time": result.get("execution_time"),
    })


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def run_code(request, exercise_id):
    """Run code against visible test cases (doesn't count as a submission)."""
    serializer = SubmitCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data["code"]

    try:
        exercise = Exercise.objects.prefetch_related("test_cases").get(
            id=exercise_id, is_published=True
        )
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update user's streak
    request.user.update_streak()

    # Run against visible test cases only
    visible_tests = exercise.test_cases.filter(is_hidden=False)
    results = _run_tests(code, visible_tests)

    submission = Submission.objects.create(
        user=request.user,
        exercise=exercise,
        code=code,
        status="passed" if all(r["passed"] for r in results) else "failed",
        passed_tests=sum(1 for r in results if r["passed"]),
        total_tests=len(results),
        is_run_only=True,
    )

    # Save individual test results
    for r in results:
        TestCaseResult.objects.create(
            submission=submission,
            test_case=r["test_case"],
            passed=r["passed"],
            actual_output=r["actual_output"],
            expected_output=r["expected_output"],
            error_message=r.get("error", ""),
            execution_time=r.get("execution_time"),
        )

    return Response(SubmissionSerializer(submission).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def submit_code(request, exercise_id):
    """Submit code for grading against all test cases (visible + hidden)."""
    serializer = SubmitCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data["code"]

    try:
        exercise = Exercise.objects.prefetch_related("test_cases", "hints").get(
            id=exercise_id, is_published=True
        )
    except Exercise.DoesNotExist:
        return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    request.user.update_streak()

    # Run against ALL test cases
    all_tests = exercise.test_cases.all()
    results = _run_tests(code, all_tests)

    all_passed = all(r["passed"] for r in results)

    submission = Submission.objects.create(
        user=request.user,
        exercise=exercise,
        code=code,
        status="passed" if all_passed else "failed",
        passed_tests=sum(1 for r in results if r["passed"]),
        total_tests=len(results),
        is_run_only=False,
    )

    for r in results:
        TestCaseResult.objects.create(
            submission=submission,
            test_case=r["test_case"],
            passed=r["passed"],
            actual_output=r["actual_output"],
            expected_output=r["expected_output"],
            error_message=r.get("error", ""),
            execution_time=r.get("execution_time"),
        )

    # Update progress and award XP if all tests passed
    if all_passed:
        progress, _ = UserExerciseProgress.objects.get_or_create(
            user=request.user, exercise=exercise
        )
        progress.attempts += 1

        if not progress.is_completed:
            # Calculate XP with hint penalty
            xp = exercise.xp_value
            total_penalty = 0
            for hint in exercise.hints.filter(level__lte=progress.hints_used):
                total_penalty += hint.xp_penalty_percent
            total_penalty = min(total_penalty, 100)
            xp_awarded = max(0, xp - int(xp * total_penalty / 100))

            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.xp_earned = xp_awarded
            progress.best_code = code
            progress.save()

            submission.xp_awarded = xp_awarded
            submission.save(update_fields=["xp_awarded"])

            request.user.award_xp(xp_awarded)

            # Check if this completes the lesson/module
            _check_module_completion(request.user, exercise.lesson.module)
        else:
            progress.save(update_fields=["attempts"])
    else:
        # Track attempt even on failure
        progress, _ = UserExerciseProgress.objects.get_or_create(
            user=request.user, exercise=exercise
        )
        progress.attempts += 1
        progress.save(update_fields=["attempts"])

    return Response(SubmissionSerializer(submission).data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def submission_history(request, exercise_id):
    """Get the user's submission history for an exercise."""
    submissions = Submission.objects.filter(
        user=request.user, exercise_id=exercise_id, is_run_only=False
    ).prefetch_related("test_results")[:10]
    return Response(SubmissionSerializer(submissions, many=True).data)


def _run_tests(code, test_cases):
    """Run code against a set of test cases and return results."""
    results = []
    for tc in test_cases:
        result = execute_code(code, input_data=tc.input_data)
        passed = False
        actual = result.get("output", "").strip()
        expected = tc.expected_output.strip()

        if result["status"] == "success":
            passed = compare_output(actual, expected)
        elif result["status"] == "error":
            actual = result.get("error", "Error during execution")

        results.append(
            {
                "test_case": tc,
                "passed": passed,
                "actual_output": actual,
                "expected_output": expected,
                "error": result.get("error", ""),
                "execution_time": result.get("execution_time"),
            }
        )
    return results

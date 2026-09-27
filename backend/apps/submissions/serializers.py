from rest_framework import serializers

from .models import Submission, TestCaseResult


class TestCaseResultSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="test_case.description", read_only=True)
    is_hidden = serializers.BooleanField(source="test_case.is_hidden", read_only=True)

    class Meta:
        model = TestCaseResult
        fields = (
            "id",
            "passed",
            "actual_output",
            "expected_output",
            "error_message",
            "execution_time",
            "description",
            "is_hidden",
        )


class SubmissionSerializer(serializers.ModelSerializer):
    test_results = TestCaseResultSerializer(many=True, read_only=True)
    exercise_title = serializers.CharField(source="exercise.title", read_only=True)

    class Meta:
        model = Submission
        fields = (
            "id",
            "exercise",
            "exercise_title",
            "code",
            "status",
            "passed_tests",
            "total_tests",
            "execution_time",
            "error_message",
            "xp_awarded",
            "is_run_only",
            "test_results",
            "created_at",
        )
        read_only_fields = (
            "status",
            "passed_tests",
            "total_tests",
            "execution_time",
            "error_message",
            "xp_awarded",
        )


class SubmitCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

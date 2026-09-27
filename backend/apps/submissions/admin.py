from django.contrib import admin

from .models import Submission, TestCaseResult


class TestCaseResultInline(admin.TabularInline):
    model = TestCaseResult
    extra = 0
    readonly_fields = ("test_case", "passed", "actual_output", "expected_output", "error_message")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "exercise", "status", "passed_tests", "total_tests", "created_at")
    list_filter = ("status", "is_run_only")
    inlines = [TestCaseResultInline]


@admin.register(TestCaseResult)
class TestCaseResultAdmin(admin.ModelAdmin):
    list_display = ("submission", "test_case", "passed")
    list_filter = ("passed",)

from django.db import models


class Submission(models.Model):
    """A code submission for an exercise."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("passed", "Passed"),
        ("failed", "Failed"),
        ("error", "Error"),
        ("timeout", "Timeout"),
    ]

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="submissions"
    )
    exercise = models.ForeignKey(
        "curriculum.Exercise", on_delete=models.CASCADE, related_name="submissions"
    )
    code = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    passed_tests = models.PositiveIntegerField(default=0)
    total_tests = models.PositiveIntegerField(default=0)
    execution_time = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True, default="")
    xp_awarded = models.PositiveIntegerField(default=0)
    is_run_only = models.BooleanField(
        default=False,
        help_text="True if this was a 'Run' (test) not a 'Submit'.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.exercise.title} ({self.status})"


class TestCaseResult(models.Model):
    """Result of running a single test case."""

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="test_results"
    )
    test_case = models.ForeignKey(
        "curriculum.TestCase", on_delete=models.CASCADE, related_name="results"
    )
    passed = models.BooleanField(default=False)
    actual_output = models.TextField(blank=True, default="")
    expected_output = models.TextField(blank=True, default="")
    error_message = models.TextField(blank=True, default="")
    execution_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.test_case}"

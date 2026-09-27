"""Real API/database/runner tests for learning progress and account ownership."""

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import (
    UserExerciseProgress,
    UserLessonProgress,
    UserModuleProgress,
)
from apps.curriculum.models import (
    Exercise,
    Hint,
    Lesson,
    Module,
    TestCase as ExerciseCase,
)
from apps.submissions.models import Submission


class LearningFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="learner", email="learner@example.invalid"
        )
        cls.other = get_user_model().objects.create_user(
            username="other", email="other@example.invalid"
        )
        cls.module = Module.objects.create(title="Start", slug="start", order=1)
        cls.next_module = Module.objects.create(title="Next", slug="next", order=2)
        cls.concept = Lesson.objects.create(
            module=cls.module, title="Concept", slug="concept", order=1
        )
        cls.lesson = Lesson.objects.create(
            module=cls.module,
            title="Code",
            slug="code",
            order=2,
            lesson_type="exercise",
        )
        cls.exercise = Exercise.objects.create(
            lesson=cls.lesson, title="Echo", slug="echo", order=1, xp_value=20
        )
        ExerciseCase.objects.create(
            exercise=cls.exercise, input_data="hello", expected_output="hello"
        )
        ExerciseCase.objects.create(
            exercise=cls.exercise,
            input_data="hidden",
            expected_output="hidden",
            is_hidden=True,
        )
        Hint.objects.create(
            exercise=cls.exercise, level=1, content="Use input", xp_penalty_percent=10
        )

    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def post(self, name, value, body=None):
        return self.client.post(reverse(name, args=[value]), body or {}, format="json")

    def test_full_learning_flow_awards_xp_once_and_unlocks_next_module(self):
        hints = self.client.get(reverse("revealed-hints", args=[self.exercise.pk]))
        self.assertEqual(hints.json(), [])
        self.assertEqual(self.post("reveal-hint", self.exercise.pk).status_code, 200)
        self.assertEqual(self.post("reveal-hint", self.exercise.pk).status_code, 404)
        hints = self.client.get(
            reverse("revealed-hints", args=[self.exercise.pk])
        ).json()
        self.assertEqual(hints[0]["content"], "Use input")
        self.assertEqual(
            self.post("mark-lesson-complete", self.lesson.pk).status_code, 400
        )
        for _ in range(2):
            self.assertEqual(
                self.post("mark-lesson-complete", self.concept.pk).status_code, 200
            )
        self.assertFalse(
            UserModuleProgress.objects.filter(
                user=self.user, module=self.module, is_completed=True
            ).exists()
        )
        response = self.post("run-code", self.exercise.pk, {"code": "print(input())"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_tests"], 1)
        self.assertEqual(response.json()["xp_awarded"], 0)
        self.assertEqual(
            self.client.get(
                reverse("submission-history", args=[self.exercise.pk])
            ).json(),
            [],
        )
        response = self.post(
            "submit-code", self.exercise.pk, {"code": 'print("wrong")'}
        )
        self.assertEqual(response.json()["status"], "failed")
        response = self.post(
            "submit-code", self.exercise.pk, {"code": "print(input())"}
        )
        self.assertEqual(response.json()["status"], "passed")
        self.assertEqual(response.json()["total_tests"], 2)
        hidden = [item for item in response.json()["test_results"] if item["is_hidden"]]
        self.assertEqual(hidden[0]["expected_output"], "")
        self.assertEqual(response.json()["xp_awarded"], 18)
        self.assertTrue(
            UserLessonProgress.objects.get(
                user=self.user, lesson=self.lesson
            ).is_completed
        )
        self.assertTrue(
            UserModuleProgress.objects.get(
                user=self.user, module=self.module
            ).is_completed
        )
        self.assertTrue(
            UserModuleProgress.objects.get(
                user=self.user, module=self.next_module
            ).is_unlocked
        )
        repeat = self.post("submit-code", self.exercise.pk, {"code": "print(input())"})
        self.assertEqual(repeat.json()["xp_awarded"], 0)
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_xp, 18)
        self.assertEqual(self.user.current_streak, 1)
        self.assertEqual(
            UserExerciseProgress.objects.get(
                user=self.user, exercise=self.exercise
            ).attempts,
            3,
        )

    def test_history_and_progress_do_not_cross_account_boundaries(self):
        self.post("submit-code", self.exercise.pk, {"code": "print(input())"})
        self.post("reveal-hint", self.exercise.pk)
        self.client.force_authenticate(self.other)
        self.assertEqual(
            self.client.get(
                reverse("submission-history", args=[self.exercise.pk])
            ).json(),
            [],
        )
        self.assertEqual(
            self.client.get(reverse("revealed-hints", args=[self.exercise.pk])).json(),
            [],
        )
        detail = self.client.get(
            reverse("exercise-detail", args=["start", "code", "echo"])
        ).json()
        self.assertFalse(detail["is_completed"])
        self.assertEqual(detail["user_attempts"], 0)
        self.assertEqual(len(detail["test_cases"]), 1)
        self.assertNotIn("solution_code", detail)

    def test_run_reports_code_errors_without_awarding_credit(self):
        response = self.post(
            "run-code", self.exercise.pk, {"code": "print(missing_name)"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "failed")
        self.assertIn("Name Error", response.json()["test_results"][0]["error_message"])
        self.assertFalse(
            UserExerciseProgress.objects.filter(
                user=self.user, is_completed=True
            ).exists()
        )

    def test_invalid_targets_and_payloads_never_create_submissions(self):
        for name in ("run-code", "submit-code", "reveal-hint", "mark-lesson-complete"):
            self.assertEqual(
                self.post(name, 99999, {"code": "print(1)"}).status_code, 404
            )
        self.assertEqual(
            self.post(
                "submit-code", self.exercise.pk, {"code": "x" * 10_001}
            ).status_code,
            400,
        )
        self.assertEqual(
            self.post("submit-code", self.exercise.pk, {"code": ""}).status_code, 400
        )
        self.assertEqual(
            self.client.get(reverse("revealed-hints", args=[99999])).status_code, 404
        )
        self.assertEqual(Submission.objects.count(), 0)

    def test_unauthenticated_code_execution_is_denied(self):
        self.client.force_authenticate(None)
        for name, args in (
            ("sandbox-run", []),
            ("run-code", [self.exercise.pk]),
            ("submit-code", [self.exercise.pk]),
        ):
            response = self.client.post(
                reverse(name, args=args), {"code": "print(1)"}, format="json"
            )
            self.assertEqual(response.status_code, 401)
        self.assertEqual(Submission.objects.count(), 0)

    def test_sandbox_returns_real_program_output(self):
        response = self.client.post(
            reverse("sandbox-run"), {"code": "print(sum(range(5)))"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["output"], "10\n")

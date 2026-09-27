"""Critique is post-solution feedback, so it must require a solved exercise.

The endpoint is documented as "feedback on a successful submission" but never
checked, and it puts the exercise's solution_code into the prompt. Any
authenticated user could call it on an unsolved exercise and steer the model
into echoing the answer back — an answer-key disclosure, not just wasted spend.
"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from apps.curriculum.models import Exercise, Lesson, Module
from apps.submissions.models import Submission

User = get_user_model()

AI_ENABLED = dict(ANTHROPIC_API_KEY="test-key", ANTHROPIC_BASE_URL="")


@override_settings(**AI_ENABLED)
class CritiqueRequiresAPassTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="learner", email="l@example.com", password="Tr0mbone-Harbor-19"
        )
        module = Module.objects.create(title="M", slug="m", order=1)
        lesson = Lesson.objects.create(
            module=module, title="L", slug="l", order=1, lesson_type="exercise"
        )
        self.exercise = Exercise.objects.create(
            lesson=lesson,
            title="Add two numbers",
            slug="add-two",
            instructions="Add them",
            order=1,
            solution_code="print(a + b)  # SECRET-SOLUTION",
            is_published=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("ai-critique", args=[self.exercise.id])

    def _post(self):
        return self.client.post(
            self.url, {"code": "print('x')"}, content_type="application/json"
        )

    def test_denied_without_a_passing_submission(self):
        with patch("apps.ai.views.get_provider") as provider:
            provider.return_value.generate.return_value = "should not be reached"
            response = self._post()

        self.assertEqual(response.status_code, 403)
        provider.assert_not_called()

    def test_denied_when_the_submission_failed(self):
        Submission.objects.create(
            user=self.user, exercise=self.exercise, code="nope", status="failed"
        )
        with patch("apps.ai.views.get_provider") as provider:
            provider.return_value.generate.return_value = "should not be reached"
            response = self._post()

        self.assertEqual(response.status_code, 403)
        provider.assert_not_called()

    def test_another_users_pass_does_not_unlock_it(self):
        other = User.objects.create_user(
            username="someone", email="o@example.com", password="Zephyr-Cobalt-8821"
        )
        Submission.objects.create(
            user=other, exercise=self.exercise, code="ok", status="passed"
        )
        with patch("apps.ai.views.get_provider") as provider:
            provider.return_value.generate.return_value = "should not be reached"
            response = self._post()

        self.assertEqual(response.status_code, 403)
        provider.assert_not_called()

    def test_allowed_after_passing(self):
        Submission.objects.create(
            user=self.user, exercise=self.exercise, code="ok", status="passed"
        )
        with patch("apps.ai.views.get_provider") as get_provider:
            get_provider.return_value.generate.return_value = "Nice work."
            response = self._post()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["feedback"], "Nice work.")

    def test_solution_never_reaches_the_model_before_a_pass(self):
        with patch("apps.ai.views.get_provider") as get_provider:
            get_provider.return_value.generate.return_value = "should not be reached"
            self._post()

        self.assertFalse(
            get_provider.called,
            "the prompt containing solution_code was built for an unsolved exercise",
        )

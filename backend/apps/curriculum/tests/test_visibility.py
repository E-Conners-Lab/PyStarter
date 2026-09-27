"""Publication status is an API visibility boundary, including parent objects."""

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.curriculum.models import Module, Lesson, Exercise


class PublicationBoundaryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reader", email="reader@example.invalid"
        )
        cls.module = Module.objects.create(title="Public", slug="public", order=1)
        cls.lesson = Lesson.objects.create(
            module=cls.module, title="Public", slug="public", order=1
        )
        cls.exercise = Exercise.objects.create(
            lesson=cls.lesson, title="Public", slug="public", order=1
        )
        cls.draft_lesson = Lesson.objects.create(
            module=cls.module,
            title="Draft lesson",
            slug="draft",
            order=2,
            is_published=False,
        )
        cls.draft_exercise = Exercise.objects.create(
            lesson=cls.lesson,
            title="Draft exercise",
            slug="draft",
            order=2,
            is_published=False,
        )

    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.client.raise_request_exception = False

    def test_public_detail_lists_exclude_drafts(self):
        detail = self.client.get(reverse("module-detail", args=["public"])).json()
        self.assertEqual([item["slug"] for item in detail["lessons"]], ["public"])
        lesson = self.client.get(
            reverse("lesson-detail", args=["public", "public"])
        ).json()
        self.assertEqual([item["slug"] for item in lesson["exercises"]], ["public"])
        listing = self.client.get(reverse("module-list")).json()
        self.assertEqual(listing[0]["lesson_count"], 1)
        self.assertEqual(listing[0]["total_xp"], self.exercise.xp_value)

    def test_missing_details_return_404(self):
        for name, args in (
            ("lesson-detail", ["public", "missing"]),
            ("exercise-detail", ["public", "public", "missing"]),
        ):
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 404)

    def test_unpublished_parent_hides_exercise_and_state_changing_routes(self):
        self.client.force_authenticate(self.user)
        for parent in (self.module, self.lesson):
            parent.is_published = False
            parent.save(update_fields=["is_published"])
            self.assertEqual(
                self.client.get(
                    reverse("exercise-detail", args=["public", "public", "public"])
                ).status_code,
                404,
            )
            for name in ("reveal-hint", "run-code", "submit-code"):
                response = self.client.post(
                    reverse(name, args=[self.exercise.pk]),
                    {"code": "print(1)"},
                    format="json",
                )
                self.assertEqual(response.status_code, 404)
            self.assertEqual(
                self.client.get(
                    reverse("revealed-hints", args=[self.exercise.pk])
                ).status_code,
                404,
            )
            self.assertEqual(
                self.client.post(
                    reverse("mark-lesson-complete", args=[self.lesson.pk]),
                    {},
                    format="json",
                ).status_code,
                404,
            )
            parent.is_published = True
            parent.save(update_fields=["is_published"])

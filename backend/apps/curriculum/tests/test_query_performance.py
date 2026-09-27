from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework.test import APIClient

from apps.accounts.models import UserExerciseProgress, UserModuleProgress
from apps.curriculum.models import Exercise, Lesson, Module

User = get_user_model()


class ModuleListQueryPerformanceTest(TestCase):
    """Ensure ModuleListView doesn't have N+1 query issues."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="perfuser", password="testpass123", email="perf@test.com"
        )
        # Create 3 modules with 3 lessons each, 5 exercises per exercise-lesson
        for m_idx in range(1, 4):
            module = Module.objects.create(
                title=f"Module {m_idx}",
                slug=f"module-{m_idx}",
                description=f"Desc {m_idx}",
                order=m_idx,
                is_published=True,
            )
            if m_idx == 1:
                UserModuleProgress.objects.create(
                    user=cls.user, module=module, is_unlocked=True
                )
            for l_idx in range(1, 4):
                lesson = Lesson.objects.create(
                    module=module,
                    title=f"Lesson {m_idx}.{l_idx}",
                    slug=f"lesson-{m_idx}-{l_idx}",
                    order=l_idx,
                    lesson_type="exercise" if l_idx == 3 else "concept",
                    content="content",
                    is_published=True,
                )
                if l_idx == 3:
                    for e_idx in range(1, 6):
                        ex = Exercise.objects.create(
                            lesson=lesson,
                            title=f"Ex {m_idx}.{l_idx}.{e_idx}",
                            slug=f"ex-{m_idx}-{l_idx}-{e_idx}",
                            order=e_idx,
                            instructions="Do something",
                            is_published=True,
                        )
                        if m_idx == 1 and e_idx <= 3:
                            UserExerciseProgress.objects.create(
                                user=cls.user, exercise=ex, is_completed=True
                            )

    def test_module_list_query_count(self):
        """Module list should use a bounded number of queries, not N+1."""
        client = APIClient()
        client.force_authenticate(user=self.user)

        context = CaptureQueriesContext(connection)
        with context:
            response = client.get("/api/v1/curriculum/modules/")

        self.assertEqual(response.status_code, 200)
        num_queries = len(context)
        self.assertLessEqual(num_queries, 12, f"Too many queries: {num_queries}")
        self.assertGreaterEqual(num_queries, 3, f"Unexpectedly few queries: {num_queries}")

        data = response.json()
        self.assertEqual(len(data), 3)
        # Module 1 has 3/5 exercises completed = 60%
        self.assertEqual(data[0]["progress_percent"], 60)

    def test_module_list_unauthenticated_query_count(self):
        """Unauthenticated requests should also be efficient."""
        client = APIClient()

        context = CaptureQueriesContext(connection)
        with context:
            response = client.get("/api/v1/curriculum/modules/")

        self.assertEqual(response.status_code, 200)
        num_queries = len(context)
        self.assertLessEqual(num_queries, 6, f"Too many queries: {num_queries}")


class LessonDetailQueryPerformanceTest(TestCase):
    """Ensure LessonDetailView uses prefetched data."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="lessonperfuser", password="testpass123", email="lessonperf@test.com"
        )
        cls.module = Module.objects.create(
            title="Test Module",
            slug="test-module",
            description="Test",
            order=1,
            is_published=True,
        )
        cls.lesson = Lesson.objects.create(
            module=cls.module,
            title="Test Lesson",
            slug="test-lesson",
            order=1,
            lesson_type="exercise",
            content="content",
            is_published=True,
        )
        for i in range(1, 6):
            ex = Exercise.objects.create(
                lesson=cls.lesson,
                title=f"Exercise {i}",
                slug=f"exercise-{i}",
                order=i,
                instructions="Do it",
                is_published=True,
            )
            if i <= 3:
                UserExerciseProgress.objects.create(
                    user=cls.user, exercise=ex, is_completed=True
                )

    def test_lesson_detail_query_count(self):
        """Lesson detail with 5 exercises should use bounded queries."""
        client = APIClient()
        client.force_authenticate(user=self.user)

        context = CaptureQueriesContext(connection)
        with context:
            response = client.get(
                f"/api/v1/curriculum/modules/{self.module.slug}/"
                f"lessons/{self.lesson.slug}/"
            )

        self.assertEqual(response.status_code, 200)
        num_queries = len(context)
        self.assertLessEqual(num_queries, 6, f"Too many queries: {num_queries}")
        self.assertGreaterEqual(num_queries, 2, f"Unexpectedly few queries: {num_queries}")

        exercises = response.json()["exercises"]
        self.assertEqual(len(exercises), 5)
        # First 3 should be completed
        completed = [e for e in exercises if e["is_completed"]]
        self.assertEqual(len(completed), 3)

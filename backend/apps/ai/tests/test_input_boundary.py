"""AI requests must reject malformed data before any paid provider call."""
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from apps.curriculum.models import Module, Lesson, Exercise


@override_settings(ANTHROPIC_API_KEY='test-only-placeholder', ANTHROPIC_BASE_URL='')
class AIInputBoundaryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(get_user_model().objects.create_user(username='boundary'))
        module = Module.objects.create(title='M', slug='m', order=1)
        lesson = Lesson.objects.create(module=module, title='L', slug='l', order=1)
        self.exercise = Exercise.objects.create(lesson=lesson, title='E', slug='e', order=1, is_published=True)
        self.url = f'/api/v1/ai/hint/{self.exercise.pk}/'

    def test_invalid_types_and_oversized_inputs_never_reach_provider(self):
        for payload in ({'code': []}, {'code': 42}, {'code': 'x' * 10001}, {'error': {}}, {'error': 'x' * 5001}):
            with self.subTest(payload_type=str(type(payload))), patch('apps.ai.views.get_provider') as provider:
                provider.return_value.generate.return_value = 'unexpected provider call'
                response = self.client.post(self.url, payload, format='json')
                self.assertEqual(response.status_code, 400)
                provider.assert_not_called()

    def test_code_is_redacted_and_delimited_before_provider(self):
        with patch('apps.ai.views.get_provider') as provider:
            provider.return_value.generate.return_value = 'Consider a loop.'
            response = self.client.post(self.url, {'code': 'api_key = "synthetic-secret-value"\nprint(1)'}, format='json')  # nosec: synthetic redaction fixture
        self.assertEqual(response.status_code, 200)
        system, prompt = provider.return_value.generate.call_args.args
        self.assertNotIn('synthetic-secret-value', prompt)
        self.assertIn('<<USER_CONTENT>>', prompt)
        self.assertIn('untrusted', system.lower())

    def test_repeated_unconfigured_requests_return_fresh_errors(self):
        with override_settings(ANTHROPIC_API_KEY=''):
            for _ in range(2):
                response = self.client.post(self.url, {'code': 'print(1)'}, format='json')
                self.assertEqual(response.status_code, 503)

"""Password recovery must never print tokens or expose delivery failures."""
import os
from importlib.util import find_spec, module_from_spec, spec_from_file_location
import secrets
import smtplib
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import SimpleTestCase, TestCase, override_settings
from rest_framework.test import APIClient


class SourceEmailConfigurationTests(SimpleTestCase):
    def test_source_install_uses_explicit_smtp_without_console_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            spec = spec_from_file_location("config.settings.delivery_test", find_spec("config.settings.development").origin)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            config = vars(module)
        self.assertEqual(config["EMAIL_BACKEND"], "django.core.mail.backends.smtp.EmailBackend")
        self.assertEqual(config["EMAIL_HOST"], "")
        self.assertTrue(config["EMAIL_USE_TLS"])


class PasswordResetDeliveryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="mail-user", email="mail-user@example.test", password=secrets.token_urlsafe(24),
        )

    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def request_reset(self, email):
        return self.client.post("/api/v1/accounts/password-reset/", {"email": email}, format="json")

    def test_delivery_failures_keep_generic_success_and_do_not_log_content(self):
        private_text = secrets.token_urlsafe(32)
        for failure in (smtplib.SMTPException(private_text), OSError(private_text)):
            with self.subTest(failure=type(failure).__name__):
                with patch("apps.accounts.views.send_mail", side_effect=failure):
                    with self.assertLogs("apps.accounts", level="WARNING") as captured:
                        response = self.request_reset(self.user.email)
                unknown = self.request_reset("missing@example.test")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, unknown.data)
                self.assertNotIn(private_text, str(response.data))
                self.assertNotIn(private_text, " ".join(captured.output))
                self.assertNotIn(self.user.email, " ".join(captured.output))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend", EMAIL_HOST="")
    def test_unconfigured_smtp_never_attempts_delivery_or_generates_token(self):
        with patch("apps.accounts.views.send_mail") as send:
            with patch("apps.accounts.views.default_token_generator.make_token") as make_token:
                with self.assertLogs("apps.accounts", level="WARNING"):
                    response = self.request_reset(self.user.email)
        self.assertEqual(response.status_code, 200)
        send.assert_not_called()
        make_token.assert_not_called()

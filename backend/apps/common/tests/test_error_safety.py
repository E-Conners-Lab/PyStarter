"""Error and password-storage security contracts, independent of endpoint logic."""
import secrets
from types import SimpleNamespace

from django.contrib.auth.hashers import check_password, make_password
from django.test import SimpleTestCase
from rest_framework.exceptions import ValidationError

from apps.common.errors import api_exception_handler


class ErrorSafetyTests(SimpleTestCase):
    def test_unexpected_exception_never_exposes_its_message_or_traceback(self):
        sensitive_text = secrets.token_urlsafe(32)
        request = SimpleNamespace(correlation_id="test-correlation-id")
        with self.assertLogs("apps.common.errors", level="ERROR") as captured:
            response = api_exception_handler(RuntimeError(sensitive_text), {"request": request})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data["request_id"], request.correlation_id)
        self.assertNotIn(sensitive_text, str(response.data))
        self.assertNotIn(sensitive_text, " ".join(captured.output))
        self.assertNotIn("Traceback", " ".join(captured.output))
        self.assertIn(request.correlation_id, " ".join(captured.output))
        self.assertIn("RuntimeError", " ".join(captured.output))

    def test_validation_error_preserves_field_information_and_correlation(self):
        request = SimpleNamespace(correlation_id="validation-correlation")
        response = api_exception_handler(ValidationError({"code": ["Too long."]}), {"request": request})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], ["Too long."])
        self.assertEqual(response.data["request_id"], request.correlation_id)

    def test_missing_request_context_still_returns_safe_error(self):
        with self.assertLogs("apps.common.errors", level="ERROR"):
            response = api_exception_handler(RuntimeError("internal failure"), {})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data["request_id"], "unavailable")
        self.assertNotIn("internal failure", str(response.data))

    def test_password_storage_uses_argon2id_with_required_costs(self):
        candidate = secrets.token_urlsafe(32)
        encoded = make_password(candidate)
        self.assertTrue(encoded.startswith("argon2$argon2id$"))
        self.assertIn("m=19456,t=2,p=1", encoded)
        self.assertTrue(check_password(candidate, encoded))
        self.assertFalse(check_password(candidate + "wrong", encoded))
        self.assertNotIn(candidate, encoded)

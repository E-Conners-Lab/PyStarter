from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

User = get_user_model()


class PasswordResetRequestTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="resetuser",
            email="reset@example.com",
            password="OldPass123!",
        )

    def setUp(self):
        self.client = APIClient()

    def test_existing_email_sends_email(self):
        response = self.client.post(
            "/api/v1/accounts/password-reset/",
            {"email": "reset@example.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset", mail.outbox[0].subject.lower())

    def test_nonexistent_email_returns_200(self):
        """Anti-enumeration: always returns 200."""
        response = self.client.post(
            "/api/v1/accounts/password-reset/",
            {"email": "nobody@example.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_email_format_returns_400(self):
        response = self.client.post(
            "/api/v1/accounts/password-reset/",
            {"email": "not-an-email"},
        )
        self.assertEqual(response.status_code, 400)


class PasswordResetConfirmTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="confirmuser",
            email="confirm@example.com",
            password="OldPass123!",
        )

    def setUp(self):
        self.client = APIClient()
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_valid_token_resets_password(self):
        response = self.client.post(
            "/api/v1/accounts/password-reset-confirm/",
            {"uid": self.uid, "token": self.token, "new_password": "NewPass456!"},
        )
        self.assertEqual(response.status_code, 200)

        # Verify new password works
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass456!"))

    def test_invalid_token_returns_400(self):
        response = self.client.post(
            "/api/v1/accounts/password-reset-confirm/",
            {"uid": self.uid, "token": "invalid-token", "new_password": "NewPass456!"},
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_uid_returns_400(self):
        response = self.client.post(
            "/api/v1/accounts/password-reset-confirm/",
            {"uid": "invalid", "token": self.token, "new_password": "NewPass456!"},
        )
        self.assertEqual(response.status_code, 400)

    def test_short_password_returns_400(self):
        response = self.client.post(
            "/api/v1/accounts/password-reset-confirm/",
            {"uid": self.uid, "token": self.token, "new_password": "short"},
        )
        self.assertEqual(response.status_code, 400)

    def test_token_invalid_after_password_change(self):
        """After resetting, the same token should not work again."""
        self.client.post(
            "/api/v1/accounts/password-reset-confirm/",
            {"uid": self.uid, "token": self.token, "new_password": "NewPass456!"},
        )
        response = self.client.post(
            "/api/v1/accounts/password-reset-confirm/",
            {"uid": self.uid, "token": self.token, "new_password": "AnotherPass789!"},
        )
        self.assertEqual(response.status_code, 400)

"""Django's configured password validators must run on every write path.

AUTH_PASSWORD_VALIDATORS was configured but never invoked: the serializers only
enforced min_length=8, so a security review registered an account with the
literal common password "password1".
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

# Each is >= 8 characters, so min_length alone lets them through.
REJECTED = {
    "common word": "password1",
    "all numeric": "29481756",
    "looks like the username": "smoketester",
}
ACCEPTED = "Tr0mbone-Harbor-19"


class RegistrationPasswordPolicyTest(TestCase):
    def _register(self, password, username="smoketester"):
        return self.client.post(
            reverse("register"),
            {"username": username, "email": "s@example.com", "password": password},
            content_type="application/json",
        )

    def test_weak_passwords_are_rejected(self):
        for label, password in REJECTED.items():
            with self.subTest(password=label):
                response = self._register(password)
                self.assertEqual(
                    response.status_code,
                    400,
                    f"{label} password was accepted: {password!r}",
                )
                self.assertFalse(User.objects.filter(username="smoketester").exists())

    def test_strong_password_is_accepted(self):
        self.assertEqual(self._register(ACCEPTED).status_code, 201)


class PasswordResetPolicyTest(TestCase):
    """The reset path is a second way to set a password and needs the same rules."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="resetme", email="r@example.com", password=ACCEPTED
        )

    def _reset_serializer(self, password):
        from apps.accounts.serializers import PasswordResetConfirmSerializer

        return PasswordResetConfirmSerializer(
            data={"token": "irrelevant", "uid": "irrelevant", "new_password": password}
        )

    def test_weak_new_password_is_rejected(self):
        serializer = self._reset_serializer("password1")
        self.assertFalse(
            serializer.is_valid(),
            "reset accepted a common password; validators are not applied here",
        )
        self.assertIn("new_password", serializer.errors)

    def test_strong_new_password_passes_validation(self):
        serializer = self._reset_serializer("Zephyr-Cobalt-8821")
        serializer.is_valid()
        self.assertNotIn("new_password", serializer.errors)

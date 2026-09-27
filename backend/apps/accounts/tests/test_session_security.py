from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()
ACCOUNTS = "/api/v1/accounts/"


@override_settings(AUTH_RATE_LIMIT=10, AUTH_RATE_WINDOW_SECONDS=60)
class SessionSecurityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="securityuser", email="security@example.test", password="OldPass123!"
        )

    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=True)

    def csrf(self):
        response = self.client.get(ACCOUNTS + "csrf/")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_X_CSRFTOKEN=response.data["csrfToken"])

    def login(self):
        self.csrf()
        response = self.client.post(
            ACCOUNTS + "login/",
            {"username": self.user.username, "password": "OldPass123!"}, format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_X_CSRFTOKEN=response["X-CSRFToken"])
        return response

    def test_lifecycle_rejects_missing_csrf(self):
        for route in ("login/", "register/", "token/refresh/", "logout/", "password-reset/", "password-reset-confirm/"):
            with self.subTest(route=route):
                response = self.client.post(ACCOUNTS + route, {}, format="json")
                self.assertEqual(response.status_code, 403)

    def test_cookie_auth_write_requires_csrf(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = str(refresh.access_token)
        response = self.client.post(ACCOUNTS + "logout/", {}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_cookie_policy_and_expired_access_refresh(self):
        response = self.login()
        for name in ("access_token", "refresh_token"):
            self.assertTrue(response.cookies[name]["httponly"])
            self.assertEqual(response.cookies[name]["samesite"], "Strict")
        self.assertEqual(response.cookies["refresh_token"]["path"], ACCOUNTS)
        old_refresh = self.client.cookies["refresh_token"].value
        expired = AccessToken(self.client.cookies["access_token"].value)
        expired.set_exp(lifetime=timedelta(seconds=-1))
        self.client.cookies["access_token"] = str(expired)
        response = self.client.post(ACCOUNTS + "token/refresh/", {}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.client.cookies["refresh_token"].value, old_refresh)
        self.client.cookies["refresh_token"] = old_refresh
        self.assertEqual(self.client.post(ACCOUNTS + "token/refresh/", {}, format="json").status_code, 401)

    def test_logout_revokes_access_and_refresh_even_with_expired_access(self):
        self.login()
        access = self.client.cookies["access_token"].value
        refresh = self.client.cookies["refresh_token"].value
        self.client.cookies["access_token"] = "expired-invalid-access"
        self.assertEqual(self.client.post(ACCOUNTS + "logout/", {}, format="json").status_code, 200)
        self.client.cookies["access_token"] = access
        self.assertEqual(self.client.get(ACCOUNTS + "me/").status_code, 401)
        self.client.cookies["refresh_token"] = refresh
        self.assertEqual(self.client.post(ACCOUNTS + "token/refresh/", {}, format="json").status_code, 401)

    def test_password_reset_revokes_existing_access_and_refresh(self):
        self.login()
        access = self.client.cookies["access_token"].value
        refresh = self.client.cookies["refresh_token"].value
        response = self.client.post(ACCOUNTS + "password-reset-confirm/", {
            "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token": default_token_generator.make_token(self.user),
            "new_password": "NewPass456!",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.cookies["access_token"] = access
        self.assertEqual(self.client.get(ACCOUNTS + "me/").status_code, 401)
        self.client.cookies["refresh_token"] = refresh
        self.assertEqual(self.client.post(ACCOUNTS + "token/refresh/", {}, format="json").status_code, 401)

    def test_login_lockout_after_five_failures(self):
        self.csrf()
        for _ in range(5):
            response = self.client.post(ACCOUNTS + "login/", {
                "username": self.user.username, "password": "wrong-password",
            }, format="json")
            self.assertEqual(response.status_code, 401)
        response = self.client.post(ACCOUNTS + "login/", {
            "username": self.user.username, "password": "OldPass123!",
        }, format="json")
        self.assertEqual(response.status_code, 429)

    def test_authentication_rate_limited_ten_per_minute(self):
        self.csrf()
        for index in range(10):
            response = self.client.post(ACCOUNTS + "login/", {
                "username": f"unknown{index}", "password": "wrong-password",
            }, format="json")
            self.assertEqual(response.status_code, 401)
        self.assertEqual(self.client.post(ACCOUNTS + "login/", {
            "username": "another", "password": "wrong-password",
        }, format="json").status_code, 429)

    def test_protected_writes_require_csrf_for_cookie_but_not_bearer_auth(self):
        self.login()
        access = self.client.cookies["access_token"].value
        self.client.credentials()
        url = "/api/v1/submissions/sandbox/"
        self.assertEqual(self.client.post(url, {}, format="json").status_code, 403)
        bearer = APIClient(enforce_csrf_checks=True)
        bearer.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.assertEqual(bearer.post(url, {}, format="json").status_code, 400)
        # Supplying a header alongside cookies must never bypass cookie CSRF.
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.assertEqual(self.client.post(url, {}, format="json").status_code, 403)

    def test_cross_origin_request_rejected_even_with_csrf_token(self):
        self.csrf()
        response = self.client.post(ACCOUNTS + "login/", {
            "username": self.user.username, "password": "OldPass123!",
        }, format="json", HTTP_ORIGIN="https://attacker.example")
        self.assertEqual(response.status_code, 403)

    def test_inactive_user_cannot_refresh(self):
        self.login()
        User.objects.filter(pk=self.user.pk).update(is_active=False)
        response = self.client.post(ACCOUNTS + "token/refresh/", {}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_logout_revokes_access_when_refresh_cookie_is_missing(self):
        self.login()
        access = self.client.cookies["access_token"].value
        del self.client.cookies["refresh_token"]
        self.assertEqual(self.client.post(ACCOUNTS + "logout/", {}, format="json").status_code, 200)
        self.client.cookies["access_token"] = access
        self.assertEqual(self.client.get(ACCOUNTS + "me/").status_code, 401)

    def test_registration_preserves_password_whitespace_for_login(self):
        self.csrf()
        candidate = "  Whitespace-Quartz-91  "
        response = self.client.post(ACCOUNTS + "register/", {
            "username": "newlearner", "password": candidate,
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.client.credentials(HTTP_X_CSRFTOKEN=response["X-CSRFToken"])
        response = self.client.post(ACCOUNTS + "login/", {
            "username": "newlearner", "password": candidate,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_X_CSRFTOKEN=response["X-CSRFToken"])
        response = self.client.post(ACCOUNTS + "login/", {
            "username": "newlearner", "password": candidate.strip(),
        }, format="json")
        self.assertEqual(response.status_code, 401)

    def test_password_reset_preserves_password_whitespace_for_login(self):
        self.csrf()
        candidate = "  Reset-Quartz-91  "
        response = self.client.post(ACCOUNTS + "password-reset-confirm/", {
            "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token": default_token_generator.make_token(self.user),
            "new_password": candidate,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(ACCOUNTS + "login/", {
            "username": self.user.username, "password": candidate,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_X_CSRFTOKEN=response["X-CSRFToken"])
        response = self.client.post(ACCOUNTS + "login/", {
            "username": self.user.username, "password": candidate.strip(),
        }, format="json")
        self.assertEqual(response.status_code, 401)

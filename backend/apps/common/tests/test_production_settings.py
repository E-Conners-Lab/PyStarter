"""Import production settings without touching deployed secrets or services."""
import os
import runpy
import secrets
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.settings import base


class ProductionSettingsTests(SimpleTestCase):
    def load_settings(self, **overrides):
        environment = {
            "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
            "ALLOWED_HOSTS": "localhost",
            "CORS_ALLOWED_ORIGINS": "http://localhost",
            **overrides,
        }
        with patch.dict(os.environ, environment, clear=True):
            return runpy.run_module("config.settings.production")

    def test_secure_cookies_and_transport_are_the_default(self):
        production = self.load_settings()
        for key in ("SECURE_SSL_REDIRECT", "SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE"):
            self.assertTrue(production[key], key)
        self.assertTrue(production["SIMPLE_JWT"]["AUTH_COOKIE_SECURE"])
        self.assertEqual(production["CSRF_COOKIE_SAMESITE"], "Strict")
        self.assertEqual(production["SESSION_COOKIE_SAMESITE"], "Strict")
        self.assertGreaterEqual(production["SECURE_HSTS_SECONDS"], 31536000)

    def test_explicit_local_http_flags_disable_both_session_cookie_types(self):
        production = self.load_settings(
            SECURE_SSL_REDIRECT="False", SESSION_COOKIE_SECURE="False",
            CSRF_COOKIE_SECURE="False", SECURE_HSTS_SECONDS="0",
        )
        self.assertFalse(production["SECURE_SSL_REDIRECT"])
        self.assertFalse(production["SESSION_COOKIE_SECURE"])
        self.assertFalse(production["SIMPLE_JWT"]["AUTH_COOKIE_SECURE"])
        self.assertFalse(production["CSRF_COOKIE_SECURE"])

    def test_unsafe_or_missing_configuration_fails_closed(self):
        for overrides in (
            {"DJANGO_SECRET_KEY": ""}, {"DJANGO_SECRET_KEY": "short"},
            {"DJANGO_SECRET_KEY": " " * 64}, {"ALLOWED_HOSTS": " , "},
            {"CORS_ALLOWED_ORIGINS": " , "},
        ):
            with self.subTest(fields=tuple(overrides)):
                with self.assertRaises(ImproperlyConfigured):
                    self.load_settings(**overrides)

    def test_misspelled_security_flags_never_disable_protection(self):
        for key in ("SECURE_SSL_REDIRECT", "SESSION_COOKIE_SECURE", "CSRF_COOKIE_SECURE"):
            with self.subTest(setting=key):
                with self.assertRaises(ImproperlyConfigured):
                    self.load_settings(**{key: "truue"})

    def test_importing_production_does_not_mutate_other_settings(self):
        original = tuple(base.MIDDLEWARE)
        first = self.load_settings()
        second = self.load_settings()
        self.assertEqual(tuple(base.MIDDLEWARE), original)
        self.assertEqual(first["MIDDLEWARE"], second["MIDDLEWARE"])
        self.assertEqual(first["MIDDLEWARE"].count("whitenoise.middleware.WhiteNoiseMiddleware"), 1)

    def test_optional_telemetry_initializes_only_with_configured_dsn(self):
        with patch("sentry_sdk.init") as initialize:
            self.load_settings()
            initialize.assert_not_called()
            self.load_settings(SENTRY_DSN="https://public@example.invalid/1")
            initialize.assert_called_once_with(
                dsn="https://public@example.invalid/1", traces_sample_rate=0.1,
                max_request_body_size="never", send_default_pii=False,
            )

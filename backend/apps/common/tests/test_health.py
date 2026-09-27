"""Tests for the health endpoint, including the reported version."""

import re
from pathlib import Path

from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from config.settings.base import APP_VERSION

DOCKERFILE = Path(__file__).resolve().parents[3] / "Dockerfile"
ARG_APP_VERSION = re.compile(r"^ARG APP_VERSION=(\S+)", re.MULTILINE)


class HealthCheckTest(TestCase):
    def test_reports_ok_and_database_connected(self):
        response = self.client.get(reverse("health-check"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["database"], "connected")

    @override_settings(APP_VERSION="9.9.9")
    def test_reports_the_configured_version(self):
        """The version was hardcoded "1.0.0" and went stale across five releases."""
        self.assertEqual(self.client.get(reverse("health-check")).json()["version"], "9.9.9")

    def test_default_version_is_not_hardcoded_stale(self):
        response = self.client.get(reverse("health-check"))
        self.assertEqual(response.json()["version"], APP_VERSION)


class VersionDriftTest(SimpleTestCase):
    """The image tag and the version the app reports must not drift apart."""

    def test_dockerfile_default_matches_settings_default(self):
        match = ARG_APP_VERSION.search(DOCKERFILE.read_text())
        self.assertIsNotNone(match, "Dockerfile must declare `ARG APP_VERSION=<version>`")
        self.assertEqual(match.group(1), APP_VERSION)

    def test_version_is_a_release_number(self):
        self.assertRegex(APP_VERSION, r"^\d+\.\d+\.\d+$")

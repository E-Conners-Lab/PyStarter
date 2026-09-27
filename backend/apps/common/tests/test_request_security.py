"""Observable API boundary requirements for the local release."""
from django.test import TestCase
from rest_framework.test import APIClient


class RequestSecurityTests(TestCase):
    def test_private_error_has_no_store_version_and_correlation(self):
        response = APIClient().get('/api/v1/accounts/me/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers.get('Cache-Control'), 'no-store')
        self.assertEqual(response.headers.get('X-API-Version'), '1')
        self.assertRegex(response.headers.get('X-Request-ID', ''), r'^[0-9a-f]{32}$')

    def test_api_rejects_form_encoded_writes(self):
        response = APIClient().post('/api/v1/accounts/login/', {'username': 'x', 'password': 'x'})
        self.assertEqual(response.status_code, 415)

    def test_cross_site_writes_are_rejected_before_credentials(self):
        response = APIClient().post('/api/v1/accounts/login/', {}, format='json', HTTP_SEC_FETCH_SITE='cross-site')
        self.assertEqual(response.status_code, 403)

    def test_authentication_uses_argon2id(self):
        from django.contrib.auth.hashers import make_password
        encoded = make_password('synthetic-audit-value')
        self.assertTrue(encoded.startswith('argon2$argon2id$'))
        self.assertIn('m=19456,t=2,p=1', encoded)

import platform
import resource
from unittest.mock import patch

from django.test import TestCase

from apps.executor.sandbox import MEMORY_LIMIT_BYTES, _set_memory_limit, execute_code


class SetMemoryLimitTests(TestCase):
    """Tests for _set_memory_limit()."""

    @patch("apps.executor.sandbox.platform")
    @patch("resource.setrlimit")
    @patch("resource.getrlimit", return_value=(resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    def test_linux_uses_rlimit_as(self, mock_getrlimit, mock_setrlimit, mock_platform):
        mock_platform.system.return_value = "Linux"
        _set_memory_limit()
        mock_setrlimit.assert_called_once_with(
            resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, resource.RLIM_INFINITY)
        )

    @patch("apps.executor.sandbox.platform")
    @patch("resource.setrlimit")
    @patch("resource.getrlimit", return_value=(resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    def test_darwin_uses_rlimit_rss(self, mock_getrlimit, mock_setrlimit, mock_platform):
        mock_platform.system.return_value = "Darwin"
        _set_memory_limit()
        mock_setrlimit.assert_called_once_with(
            resource.RLIMIT_RSS, (MEMORY_LIMIT_BYTES, resource.RLIM_INFINITY)
        )

    def test_set_memory_limit_does_not_crash(self):
        """_set_memory_limit() should never raise, even if platform doesn't support it."""
        _set_memory_limit()

    def test_normal_code_works_with_memory_limit(self):
        """Normal code should still execute successfully."""
        result = execute_code('print("hello")')
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"].strip(), "hello")

    def test_excessive_memory_returns_error_on_linux(self):
        """On Linux, code allocating excessive memory should fail.
        On macOS, RLIMIT_RSS is advisory so the test is skipped."""
        if platform.system() != "Linux":
            self.skipTest("RLIMIT_AS enforcement only works on Linux")
        result = execute_code('x = "a" * (10 ** 9)')
        self.assertIn(result["status"], ("error", "timeout"))

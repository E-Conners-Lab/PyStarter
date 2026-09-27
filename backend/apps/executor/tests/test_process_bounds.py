"""Local runner reliability checks, not hostile-code isolation guarantees."""

import os
import time
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.executor.sandbox import _decode_result, execute_code
from apps.executor.tests.test_isolation import ESCAPE_PREAMBLE


class ProcessBoundsTests(SimpleTestCase):
    def test_beginner_type_builtin_is_available(self):
        result = execute_code("print(type(42).__name__)")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"].strip(), "int")

    def test_huge_print_output_is_bounded(self):
        result = execute_code('print("a" * 100_000)')
        self.assertEqual(result["status"], "error")
        self.assertLess(len(result["output"]), 70_000)
        self.assertIn("output", result["error"].lower())

    def test_direct_pipe_output_is_bounded(self):
        probe = ESCAPE_PREAMBLE + 'imp("os").write(1, b"a" * 1_000_000)'
        result = execute_code(probe)
        self.assertEqual(result["status"], "error")
        self.assertLess(len(result["output"]), 70_000)

    def test_transport_stderr_is_not_exposed(self):
        probe = (
            ESCAPE_PREAMBLE
            + 'imp("os").write(2, b"PRIVATE_TRACE_MARKER"); imp("os")._exit(1)'
        )
        result = execute_code(probe)
        self.assertEqual(result["status"], "error")
        self.assertNotIn("PRIVATE_TRACE_MARKER", result["error"])

    def test_child_uses_scratch_working_directory(self):
        result = execute_code(ESCAPE_PREAMBLE + 'print(imp("os").getcwd())')
        self.assertEqual(result["status"], "success")
        self.assertNotEqual(result["output"].strip(), os.getcwd())
        self.assertFalse(os.path.exists(result["output"].strip()))

    def test_descendant_holding_pipes_cannot_extend_deadline(self):
        # Bounded probe: the descendant exits itself within three seconds even
        # if the process-tree cleanup regresses.
        probe = ESCAPE_PREAMBLE + (
            'imp("subprocess").Popen([imp("sys").executable, "-c", '
            '"import time; time.sleep(3)"])\n'
            "while True: pass\n"
        )
        start = time.monotonic()
        result = execute_code(probe, timeout=0.2)
        self.assertEqual(result["status"], "timeout")
        self.assertLess(time.monotonic() - start, 1.5)

    @patch("apps.executor.sandbox.os.name", "nt")
    def test_native_windows_fails_closed_with_docker_guidance(self):
        result = execute_code('print("hello")')
        self.assertEqual(result["status"], "error")
        self.assertIn("Docker", result["error"])

    def test_successful_runner_cleans_up_background_children(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "completed"
            child_code = (
                "import time; from pathlib import Path; time.sleep(0.5); "
                f"Path({str(marker)!r}).touch()"
            )
            probe = ESCAPE_PREAMBLE + (
                f'imp("subprocess").Popen([imp("sys").executable, "-c", {child_code!r}])'
            )
            result = execute_code(probe)
            self.assertEqual(result["status"], "success")
            time.sleep(0.7)
            self.assertFalse(
                marker.exists(), "Background child survived the completed execution"
            )

    def test_malformed_child_results_are_generic_errors(self):
        for raw in (
            b'{"status": []}',
            b"[" * 2000 + b"]" * 2000,
            b'{"status": "success", "output": "", "error": "", '
            b'"execution_time": 1e999}',
        ):
            with self.subTest(raw=raw[:50]):
                result = _decode_result(raw)
                self.assertEqual(result["status"], "error")
                self.assertEqual(result["error"], "Code execution failed.")

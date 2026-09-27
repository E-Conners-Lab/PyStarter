"""Beginner-facing execution semantics, independent of process transport."""

from unittest.mock import patch
from django.test import SimpleTestCase
from apps.executor import runner
from apps.executor.sandbox import compare_output, execute_code


class ProgramBehaviorTests(SimpleTestCase):
    def run_program(self, code, input_data=""):
        # Resource caps belong to the child; these benign unit examples exercise
        # language/error behavior without lowering limits of the test process.
        with (
            patch.object(runner, "_set_memory_limit"),
            patch.object(runner.sys, "setrecursionlimit"),
        ):
            return runner.run(code, input_data)

    def test_allowed_libraries_and_prompted_input(self):
        result = self.run_program(
            'import math\nx = float(input("Number: "))\nprint(math.sqrt(x))', "9"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "Number: 3.0\n")

    def test_exhausted_input_has_actionable_error(self):
        result = self.run_program("input(); input()", "first")
        self.assertEqual(result["status"], "error")
        self.assertIn("No more input", result["error"])

    def test_missing_input_returns_empty_string(self):
        self.assertEqual(self.run_program("print(repr(input()))")["output"], "''\n")

    def test_unavailable_import_has_learning_guidance(self):
        result = self.run_program("import subprocess")
        self.assertEqual(result["status"], "error")
        self.assertIn("Allowed modules", result["error"])

    def test_common_beginner_errors_keep_output_and_exercise_line(self):
        for code, label in (
            ("1 / 0", "Math Error"),
            ("x[0]", "Name Error"),
            ('1 + "a"', "Type Error"),
            ("[][1]", "Index Error"),
            ('{}["missing"]', "Key Error"),
            ('int("word")', "Value Error"),
            ("1.missing", "Syntax Error"),
            ('"x".missing', "Attribute Error"),
            ("  print(1)", "Indentation Error"),
        ):
            with self.subTest(label=label):
                result = self.run_program(code)
                self.assertEqual(result["status"], "error")
                self.assertIn(label, result["error"])
                self.assertIn("<exercise>", result["error"])
        result = self.run_program('print("before"); 1 / 0')
        self.assertEqual(result["output"], "before\n")

    def test_print_flood_is_a_bounded_learning_error(self):
        result = self.run_program('print("x" * 100_000)')
        self.assertEqual(result["status"], "error")
        self.assertIn("too much output", result["error"])
        self.assertLess(len(result["output"]), 16_385)

    def test_grading_accepts_formatting_and_numeric_tolerance_only(self):
        for actual, expected in [
            ("hello \n", "hello"),
            ("a \nb ", "a\nb"),
            ("0.3000000001", "0.3"),
        ]:
            self.assertTrue(compare_output(actual, expected))
        for actual, expected in [
            ("wrong", "right"),
            ("1.1", "1"),
            ("nan", "0"),
            ("inf", "infinitude"),
        ]:
            self.assertFalse(compare_output(actual, expected))

    def test_invalid_execution_requests_fail_without_spawning(self):
        with patch("apps.executor.sandbox.subprocess.Popen") as spawn:
            for kwargs in (
                {"code": None},
                {"code": "x" * 10_001},
                {"code": "", "input_data": None},
                {"code": "", "input_data": "x" * 100_001},
                {"code": "", "timeout": 0},
                {"code": "", "timeout": 31},
                {"code": "", "timeout": float("nan")},
            ):
                self.assertEqual(execute_code(**kwargs)["status"], "error")
            spawn.assert_not_called()

    def test_unavailable_scratch_storage_returns_generic_failure(self):
        with patch(
            "apps.executor.sandbox.tempfile.TemporaryDirectory",
            side_effect=OSError("private host path"),
        ):
            result = execute_code("print(1)")
        self.assertEqual(result["status"], "error")
        self.assertNotIn("private host path", result["error"])

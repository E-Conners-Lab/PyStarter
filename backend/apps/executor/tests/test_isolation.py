"""Isolation guarantees for student code execution.

These lock in the properties a security review found missing in the 1.0.6 release,
where code ran inside the Django process with a timeout that did not stop it.

What these tests do NOT claim: that the Python-level restrictions cannot be
escaped. They can be — a student can still reach real builtins through a
function's __globals__. These assert the boundary that actually contains that
escape: a separate process, without the server's secrets, that dies on deadline.
"""

import time

from django.test import SimpleTestCase

from apps.executor.sandbox import execute_code

# Big enough that an unkilled loop runs far past the deadline (~25s), so a
# regression fails loudly on the clock instead of hanging the suite forever.
RUNAWAY = "x = 0\nfor i in range(1_000_000_000):\n    x += 1\nprint(x)"

# Recovers real builtins through a Python function's __globals__ — the escape a
# security review confirmed. Used here to probe what the escape can still reach.
ESCAPE_PREAMBLE = (
    'b = input.__globals__["__builtins__"]\n'
    'try:\n'
    '    imp = b["__import__"]\n'
    'except Exception:\n'
    '    imp = b.__import__\n'
)


class TimeoutTest(SimpleTestCase):
    def test_deadline_actually_stops_the_code(self):
        start = time.time()
        result = execute_code(RUNAWAY, timeout=1)
        elapsed = time.time() - start

        self.assertEqual(result["status"], "timeout")
        self.assertLess(
            elapsed,
            5,
            "execute_code returned only after the code finished — the deadline is "
            "cosmetic and a runaway loop can occupy a worker",
        )


class ProcessIsolationTest(SimpleTestCase):
    """Student code must not reach the server's credentials, even after escaping."""

    def test_server_secrets_are_not_in_the_child_environment(self):
        probe = ESCAPE_PREAMBLE + (
            'os_mod = imp("os")\n'
            'names = ("ANTHROPIC_API_KEY", "DJANGO_SECRET_KEY", "DB_PASSWORD", "SENTRY_DSN")\n'
            'found = [n for n in names if os_mod.environ.get(n)]\n'
            'print("LEAKED:" + ",".join(found))\n'
        )
        with self.settings():
            result = execute_code(probe)

        self.assertEqual(result["status"], "success", result.get("error", ""))
        self.assertIn("LEAKED:", result["output"])
        leaked = result["output"].split("LEAKED:")[1].strip()
        self.assertEqual(leaked, "", f"student code can read server secrets: {leaked}")

    def test_runs_outside_the_django_process(self):
        probe = ESCAPE_PREAMBLE + (
            'os_mod = imp("os")\n'
            'print("PID:" + str(os_mod.getpid()))\n'
        )
        result = execute_code(probe)

        self.assertEqual(result["status"], "success", result.get("error", ""))
        child_pid = int(result["output"].split("PID:")[1].strip())
        import os as _os

        self.assertNotEqual(
            child_pid,
            _os.getpid(),
            "code executed in the web process — an escape reaches the app's database "
            "connection, credentials, and Django internals",
        )

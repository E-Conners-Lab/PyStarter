"""
Sandboxed Python code execution engine.
Orchestrates code execution in an isolated subprocess with resource limits.
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

MEMORY_LIMIT_BYTES = 128 * 1024 * 1024  # 128 MB

_RUNNER_PATH = str(Path(__file__).resolve().parent / "runner.py")


def _get_limit_type():
    """Return the appropriate resource limit type for the current platform, or None."""
    try:
        import resource  # noqa: F811
    except ImportError:
        return None  # Windows
    system = platform.system()
    if system == "Linux":
        return resource.RLIMIT_AS
    elif system == "Darwin":
        return resource.RLIMIT_RSS
    return None


def _set_memory_limit():
    """Set a memory limit for the current process.

    Uses RLIMIT_AS on Linux, RLIMIT_RSS on macOS.
    Returns the previous limits so they can be restored after execution.
    """
    limit_type = _get_limit_type()
    if limit_type is None:
        return None

    import resource

    try:
        old_soft, hard = resource.getrlimit(limit_type)
        new_soft = min(MEMORY_LIMIT_BYTES, hard) if hard != resource.RLIM_INFINITY else MEMORY_LIMIT_BYTES
        resource.setrlimit(limit_type, (new_soft, hard))
        return (limit_type, old_soft, hard)
    except (ValueError, OSError):
        return None


def _restore_memory_limit(saved):
    """Restore memory limits saved by _set_memory_limit()."""
    if saved is None:
        return
    try:
        import resource

        limit_type, old_soft, hard = saved
        resource.setrlimit(limit_type, (old_soft, hard))
    except (ValueError, OSError, ImportError):
        pass


def execute_code(code, input_data="", timeout=5):
    """
    Execute Python code in an isolated subprocess.

    Returns:
        dict with keys:
        - status: "success", "error", "timeout"
        - output: stdout output
        - error: error message (if any)
        - execution_time: time in seconds
    """
    payload = json.dumps({"code": code, "input_data": input_data})

    # Stripped environment: only PATH and Python essentials, no secrets
    safe_env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.environ.get("HOME", "/tmp"),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }

    try:
        result = subprocess.run(
            [sys.executable, _RUNNER_PATH],
            input=payload,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=safe_env,
        )
        try:
            return json.loads(result.stdout)
        except (json.JSONDecodeError, ValueError):
            return {
                "status": "error",
                "output": "",
                "error": result.stderr.strip() or "Code execution failed.",
                "execution_time": 0.0,
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": "",
            "error": f"Your code took too long to run (limit: {timeout} seconds). "
            "Check for infinite loops!",
            "execution_time": timeout,
        }


def _make_friendly_error(exception, traceback_lines):
    """Convert Python errors into beginner-friendly messages."""
    error_type = type(exception).__name__
    error_msg = str(exception)

    # Find the line number in user code
    line_info = ""
    for line in traceback_lines:
        if '<exercise>' in line:
            line_info = line.strip()
            break

    friendly_messages = {
        "SyntaxError": f"Syntax Error: Python couldn't understand your code. {error_msg}",
        "NameError": (
            f"Name Error: {error_msg}. Did you misspell a variable name, "
            "or try to use a variable before creating it?"
        ),
        "TypeError": f"Type Error: {error_msg}. You might be mixing up data types (like adding a number to a string).",
        "IndexError": f"Index Error: {error_msg}. You're trying to access an item that doesn't exist in the list.",
        "KeyError": f"Key Error: {error_msg}. That key doesn't exist in the dictionary.",
        "ValueError": f"Value Error: {error_msg}. The value isn't what Python expected.",
        "ZeroDivisionError": "Math Error: You can't divide by zero!",
        "IndentationError": (
            f"Indentation Error: {error_msg}. "
            "Python uses spaces to know which code belongs together. "
            "Check that your lines are indented correctly."
        ),
        "AttributeError": f"Attribute Error: {error_msg}. That method or property doesn't exist on this object.",
    }

    friendly = friendly_messages.get(error_type, f"{error_type}: {error_msg}")
    if line_info:
        friendly += f"\n{line_info}"
    return friendly


def compare_output(actual, expected):
    """
    Compare actual output to expected output, with some flexibility
    for beginners (trailing whitespace, etc.).
    """
    actual = actual.strip()
    expected = expected.strip()

    if actual == expected:
        return True

    # Try comparing line by line, ignoring trailing whitespace
    actual_lines = [l.rstrip() for l in actual.split("\n")]
    expected_lines = [l.rstrip() for l in expected.split("\n")]
    if actual_lines == expected_lines:
        return True

    # Try numeric comparison (for floating point tolerance)
    try:
        actual_num = float(actual)
        expected_num = float(expected)
        if abs(actual_num - expected_num) < 1e-6:
            return True
    except (ValueError, TypeError):
        pass

    return False

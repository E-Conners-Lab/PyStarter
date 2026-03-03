"""
Sandboxed Python code execution engine.
Runs user code in a restricted environment with resource limits.
"""

import io
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from contextlib import redirect_stderr, redirect_stdout

# Imports allowed for beginner exercises
ALLOWED_IMPORTS = {
    "math",
    "random",
    "string",
    "collections",
    "datetime",
    "json",
    "re",
    "typing",
    "copy",
    "itertools",
    "functools",
    "textwrap",
    "ipaddress",
}

# Builtins that are forbidden
FORBIDDEN_BUILTINS = {
    "exec",
    "eval",
    "compile",
    "open",
    "input",
    "__import__",
    "globals",
    "getattr",
    "setattr",
    "delattr",
    "breakpoint",
    "exit",
    "quit",
}


def _make_safe_builtins():
    """Create a copy of builtins with dangerous functions removed."""
    import builtins

    safe = {k: v for k, v in vars(builtins).items() if k not in FORBIDDEN_BUILTINS}

    # Replace input with a version that reads from our fake stdin
    def safe_input(prompt=""):
        # This will be overridden per-execution with proper stdin
        return ""

    safe["input"] = safe_input
    return safe


def _make_safe_import(allowed):
    """Create a restricted __import__ that only allows specific modules."""

    original_import = __import__

    def restricted_import(name, *args, **kwargs):
        top_level = name.split(".")[0]
        if top_level not in allowed:
            raise ImportError(
                f"Module '{name}' is not available. "
                f"Allowed modules: {', '.join(sorted(allowed))}"
            )
        return original_import(name, *args, **kwargs)

    return restricted_import


def execute_code(code, input_data="", timeout=5):
    """
    Execute Python code in a sandboxed environment.

    Returns:
        dict with keys:
        - status: "success", "error", "timeout"
        - output: stdout output
        - error: error message (if any)
        - execution_time: time in seconds
    """

    def _run():
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Build safe globals
        safe_builtins = _make_safe_builtins()
        safe_builtins["__import__"] = _make_safe_import(ALLOWED_IMPORTS)

        # If there's input data, create a fake stdin
        if input_data:
            fake_stdin = io.StringIO(input_data)
            input_lines = iter(input_data.strip().split("\n"))

            def safe_input(prompt=""):
                # Print the prompt (like real input() does)
                if prompt:
                    stdout_capture.write(str(prompt))
                try:
                    return next(input_lines)
                except StopIteration:
                    raise EOFError("No more input available")

            safe_builtins["input"] = safe_input

        safe_globals = {"__builtins__": safe_builtins, "__name__": "__main__"}

        start_time = time.time()
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                compiled = compile(code, "<exercise>", "exec")
                exec(compiled, safe_globals)  # noqa: S102

            execution_time = time.time() - start_time
            return {
                "status": "success",
                "output": stdout_capture.getvalue(),
                "error": "",
                "execution_time": round(execution_time, 4),
            }
        except Exception as e:
            execution_time = time.time() - start_time
            # Format a beginner-friendly error message
            tb = traceback.format_exc()
            # Extract just the relevant part of the traceback
            lines = tb.strip().split("\n")
            friendly_error = _make_friendly_error(e, lines)
            return {
                "status": "error",
                "output": stdout_capture.getvalue(),
                "error": friendly_error,
                "execution_time": round(execution_time, 4),
            }

    # Run with timeout
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_run)
        try:
            result = future.result(timeout=timeout)
            return result
        except TimeoutError:
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

    # Try case-insensitive comparison for simple string outputs
    if actual.lower() == expected.lower():
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

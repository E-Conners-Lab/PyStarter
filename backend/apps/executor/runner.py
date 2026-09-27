"""
Standalone subprocess runner for trusted local Python code execution.
Invoked by sandbox.py via subprocess — never imported by Django directly.

Accepts JSON on stdin: {"code": "...", "input_data": "..."}
Prints JSON to stdout: {"status": "...", "output": "...", "error": "...", "execution_time": 0.0}
"""

import io
import json
import sys
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout

MEMORY_LIMIT_BYTES = 128 * 1024 * 1024  # 128 MB
MAX_OUTPUT_CHARS = 16_384
MAX_ERROR_CHARS = 2_048


class OutputLimitExceeded(Exception):
    """The local program exceeded its display output budget."""


class BoundedOutput(io.StringIO):
    def write(self, value):
        if self.tell() + len(value) > MAX_OUTPUT_CHARS:
            raise OutputLimitExceeded("Your code produced too much output.")
        return super().write(value)


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
    "vars",
    "dir",
    "hasattr",
    "object",
    "super",
}


def _set_memory_limit():
    """Set a memory limit for the current process."""
    try:
        import platform
        import resource
    except ImportError:
        return

    system = platform.system()
    if system == "Linux":
        limit_type = resource.RLIMIT_AS
    elif system == "Darwin":
        limit_type = resource.RLIMIT_RSS
    else:
        return

    try:
        _, hard = resource.getrlimit(limit_type)
        new_soft = (
            min(MEMORY_LIMIT_BYTES, hard)
            if hard != resource.RLIM_INFINITY
            else MEMORY_LIMIT_BYTES
        )
        resource.setrlimit(limit_type, (new_soft, hard))
    except (ValueError, OSError):
        pass


def _make_safe_builtins():
    """Create a copy of builtins with dangerous functions removed."""
    import builtins

    safe = {k: v for k, v in vars(builtins).items() if k not in FORBIDDEN_BUILTINS}

    def safe_input(prompt=""):
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


def _make_friendly_error(exception, traceback_lines):
    """Convert Python errors into beginner-friendly messages."""
    error_type = type(exception).__name__
    error_msg = str(exception)

    line_info = ""
    for line in traceback_lines:
        if "<exercise>" in line:
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


def run(code, input_data=""):
    """Execute code in a restricted environment."""
    _set_memory_limit()
    sys.setrecursionlimit(200)

    stdout_capture = BoundedOutput()
    stderr_capture = BoundedOutput()

    safe_builtins = _make_safe_builtins()
    safe_builtins["__import__"] = _make_safe_import(ALLOWED_IMPORTS)

    if input_data:
        input_lines = iter(input_data.strip().split("\n"))

        def safe_input(prompt=""):
            if prompt:
                stdout_capture.write(str(prompt))
            try:
                return next(input_lines)
            except StopIteration:
                raise EOFError("No more input available")

        safe_builtins["input"] = safe_input

    safe_globals = {"__builtins__": safe_builtins, "__name__": "__main__"}

    start_time = time.monotonic()
    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            compiled = compile(code, "<exercise>", "exec")
            exec(compiled, safe_globals)  # noqa: S102

        execution_time = time.monotonic() - start_time
        return {
            "status": "success",
            "output": stdout_capture.getvalue(),
            "error": "",
            "execution_time": round(execution_time, 4),
        }
    except Exception as e:
        execution_time = time.monotonic() - start_time
        tb = traceback.format_exc()
        lines = tb.strip().split("\n")
        friendly_error = _make_friendly_error(e, lines)
        return {
            "status": "error",
            "output": stdout_capture.getvalue(),
            "error": friendly_error[:MAX_ERROR_CHARS],
            "execution_time": round(execution_time, 4),
        }


if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    result = run(payload.get("code", ""), payload.get("input_data", ""))
    print(json.dumps(result))

"""
Trusted local Python runner.
A subprocess limits accidental resource use; it is not a security boundary.
"""

import json
import os
import platform
import selectors
import signal
import tempfile
import time
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
        new_soft = (
            min(MEMORY_LIMIT_BYTES, hard)
            if hard != resource.RLIM_INFINITY
            else MEMORY_LIMIT_BYTES
        )
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


MAX_CAPTURE_BYTES = 256 * 1024
MAX_CODE_CHARS = 10_000
MAX_INPUT_CHARS = 100_000
MAX_OUTPUT_CHARS = 16_384
MAX_ERROR_CHARS = 2_048
MAX_TIMEOUT_SECONDS = 30


def _error(message, status="error", elapsed=0.0):
    return {"status": status, "output": "", "error": message, "execution_time": elapsed}


def _kill_process_group(process):
    """Clean up descendants in our session, including after the runner exits.

    Deliberately hostile code can create another session. This is a reliability
    control for trusted local code, not a hostile process containment boundary.
    """
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass  # The whole process group already exited.
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        process.kill()


def _collect_output(process, deadline):
    """Drain bounded output without waiting indefinitely on descendant pipes."""
    chunks = []
    captured = 0
    with selectors.DefaultSelector() as selector:
        for stream in (process.stdout, process.stderr):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None, "timeout"
            ready = selector.select(min(remaining, 0.05))
            if not ready and process.poll() is not None:
                break  # A background child may still own a pipe; clean it up.
            for key, _ in ready:
                data = os.read(key.fileobj.fileno(), 8192)
                if not data:
                    selector.unregister(key.fileobj)
                    continue
                captured += len(data)
                if captured > MAX_CAPTURE_BYTES:
                    return None, "output"
                if key.fileobj is process.stdout:
                    chunks.append(data)
    try:
        process.wait(timeout=max(0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        return None, "timeout"
    return b"".join(chunks), None


def _decode_result(raw):
    """Never pass child transport errors or unvalidated fields to the API."""
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeError, RecursionError):
        return _error("Code execution failed.")
    if not isinstance(result, dict) or result.get("status") not in ("success", "error"):
        return _error("Code execution failed.")
    output, error, elapsed = (
        result.get(key) for key in ("output", "error", "execution_time")
    )
    if not isinstance(output, str) or not isinstance(error, str):
        return _error("Code execution failed.")
    if type(elapsed) not in (int, float) or not 0 <= elapsed <= MAX_TIMEOUT_SECONDS:
        return _error("Code execution failed.")
    if len(output) > MAX_OUTPUT_CHARS:
        return _error("Your code produced too much output.")
    return {
        "status": result["status"],
        "output": output,
        "error": error[:MAX_ERROR_CHARS],
        "execution_time": round(elapsed, 4),
    }


def _execute_in_directory(payload, directory, timeout):
    # The environment reduction prevents accidental inheritance. Same-user code
    # can still access host files/processes; do not call this secret isolation.
    safe_env = {"PATH": os.defpath, "HOME": directory, "LANG": "C.UTF-8"}
    deadline = time.monotonic() + timeout
    with tempfile.TemporaryFile() as stdin:
        stdin.write(payload)
        stdin.seek(0)
        process = subprocess.Popen(
            [sys.executable, "-I", _RUNNER_PATH],
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=directory,
            env=safe_env,
            start_new_session=True,
        )
        try:
            raw, failure = _collect_output(process, deadline)
        finally:
            _kill_process_group(process)
            process.stdout.close()
            process.stderr.close()
    if failure == "timeout":
        return _error(
            f"Your code took too long to run (limit: {timeout} seconds). "
            "Check for infinite loops!",
            "timeout",
            timeout,
        )
    if failure == "output":
        return _error("Your code produced too much output.")
    if process.returncode:
        return _error("Code execution failed.")
    return _decode_result(raw)


def execute_code(code, input_data="", timeout=5):
    """Execute trusted local code with best-effort resource/deadline controls."""
    if os.name != "posix":
        return _error(
            "Code execution requires Docker on Windows. Start the Docker installation."
        )
    if not isinstance(code, str) or len(code) > MAX_CODE_CHARS:
        return _error("Code exceeds the execution size limit.")
    if not isinstance(input_data, str) or len(input_data) > MAX_INPUT_CHARS:
        return _error("Input exceeds the execution size limit.")
    if not isinstance(timeout, (int, float)) or not 0 < timeout <= MAX_TIMEOUT_SECONDS:
        return _error("Invalid execution timeout.")
    payload = json.dumps({"code": code, "input_data": input_data}).encode("utf-8")
    try:
        with tempfile.TemporaryDirectory(prefix="pystarter-run-") as directory:
            return _execute_in_directory(payload, directory, timeout)
    except (OSError, ValueError):
        return _error("Code execution is temporarily unavailable.")


def _make_friendly_error(exception, traceback_lines):
    """Convert Python errors into beginner-friendly messages."""
    error_type = type(exception).__name__
    error_msg = str(exception)

    # Find the line number in user code
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
    actual_lines = [line.rstrip() for line in actual.split("\n")]
    expected_lines = [line.rstrip() for line in expected.split("\n")]
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

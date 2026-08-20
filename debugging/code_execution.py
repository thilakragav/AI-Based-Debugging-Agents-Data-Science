import ast
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict


DEFAULT_TIMEOUT = 10


# =========================================================
# UNSAFE IMPORTS / OPERATIONS
# =========================================================

BLOCKED_MODULES = {
    "os",
    "subprocess",
    "shutil",
    "socket",
    "requests",
    "urllib",
    "http",
    "ftplib",
    "paramiko",
}

BLOCKED_CALLS = {
    "eval",
    "exec",
    "compile",
    "__import__",
    "open",
}


# =========================================================
# CODE SAFETY CHECK
# =========================================================

def validate_code_safety(code: str) -> Dict[str, Any]:
    """
    Perform a basic static safety check before execution.

    This is NOT a complete security sandbox.
    It is an additional protection layer for the PoC.
    """

    if not code or not code.strip():
        return {
            "safe": False,
            "reason": "No corrected code was provided."
        }

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return {
            "safe": False,
            "reason": f"Corrected code contains a syntax error: {exc}"
        }

    for node in ast.walk(tree):

        # -------------------------------------------------
        # Block dangerous imports
        # -------------------------------------------------

        if isinstance(node, ast.Import):

            for alias in node.names:

                module = alias.name.split(".")[0]

                if module in BLOCKED_MODULES:
                    return {
                        "safe": False,
                        "reason": (
                            f"Blocked module import: {module}"
                        )
                    }

        # -------------------------------------------------
        # Block from-import
        # -------------------------------------------------

        elif isinstance(node, ast.ImportFrom):

            module = (node.module or "").split(".")[0]

            if module in BLOCKED_MODULES:
                return {
                    "safe": False,
                    "reason": (
                        f"Blocked module import: {module}"
                    )
                }

        # -------------------------------------------------
        # Block dangerous function calls
        # -------------------------------------------------

        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id in BLOCKED_CALLS:
                    return {
                        "safe": False,
                        "reason": (
                            f"Blocked function call: {node.func.id}"
                        )
                    }

    return {
        "safe": True,
        "reason": "Static safety checks passed."
    }


# =========================================================
# EXECUTE PYTHON CODE
# =========================================================

def execute_python_code(
    code: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    Execute corrected Python code in a temporary directory.

    Returns structured execution evidence.
    """

    safety = validate_code_safety(code)

    if not safety["safe"]:

        return {
            "executed": False,
            "status": "BLOCKED",
            "reason": safety["reason"],
            "stdout": "",
            "stderr": "",
            "return_code": None,
        }

    temporary_directory = tempfile.mkdtemp(
        prefix="ai_debug_execution_"
    )

    script_path = Path(
        temporary_directory
    ) / "corrected_code.py"

    try:

        script_path.write_text(
            code,
            encoding="utf-8"
        )

        environment = os.environ.copy()

        # Prevent Python from writing .pyc files.
        environment["PYTHONDONTWRITEBYTECODE"] = "1"

        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
            ],
            cwd=temporary_directory,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
            env=environment,
        )

        if result.returncode == 0:

            status = "PASS"

        else:

            status = "FAIL"

        return {
            "executed": True,
            "status": status,
            "reason": (
                "Code executed successfully."
                if status == "PASS"
                else "Corrected code still produced an error."
            ),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    except subprocess.TimeoutExpired as exc:

        return {
            "executed": False,
            "status": "TIMEOUT",
            "reason": (
                f"Execution exceeded {timeout} seconds."
            ),
            "stdout": (
                exc.stdout.decode(errors="replace")
                if isinstance(exc.stdout, bytes)
                else (exc.stdout or "")
            ),
            "stderr": (
                exc.stderr.decode(errors="replace")
                if isinstance(exc.stderr, bytes)
                else (exc.stderr or "")
            ),
            "return_code": None,
        }

    except Exception as exc:

        return {
            "executed": False,
            "status": "ERROR",
            "reason": str(exc),
            "stdout": "",
            "stderr": "",
            "return_code": None,
        }

    finally:

        # Remove temporary execution directory.
        try:

            for file in Path(
                temporary_directory
            ).glob("*"):

                file.unlink(
                    missing_ok=True
                )

            Path(
                temporary_directory
            ).rmdir()

        except Exception:
            pass
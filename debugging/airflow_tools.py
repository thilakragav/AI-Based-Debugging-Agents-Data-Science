import platform
import subprocess
import shutil
from pathlib import Path


# =========================================================
# RUN COMMAND
# =========================================================

def run_command(command):

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": "Command timed out."
        }

    except FileNotFoundError:

        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": (
                f"Command not found: {command[0]}"
            )
        }

    except Exception as e:

        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": str(e)
        }


# =========================================================
# CHECK AIRFLOW INSTALLATION
# =========================================================

def check_airflow_installation():

    airflow_path = shutil.which("airflow")

    if not airflow_path:

        return {
            "installed": False,
            "airflow_path": None,
            "version": None,
            "message": (
                "Airflow executable was not found "
                "in the current environment."
            )
        }

    version = run_command(
        ["airflow", "version"]
    )

    return {
        "installed": True,
        "airflow_path": airflow_path,
        "version": version
    }


# =========================================================
# CHECK AIRFLOW VERSION
# =========================================================

def check_airflow_version():

    result = run_command(
        ["airflow", "version"]
    )

    return {
        "success": result["success"],
        "version": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# LIST AIRFLOW DAGS
# =========================================================

def check_airflow_dags():

    result = run_command(
        [
            "airflow",
            "dags",
            "list"
        ]
    )

    return {
        "success": result["success"],
        "output": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# CHECK DAG IMPORT ERRORS
# =========================================================

def check_dag_import_errors():

    result = run_command(
        [
            "airflow",
            "dags",
            "list-import-errors"
        ]
    )

    return {
        "success": result["success"],
        "import_errors": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# CHECK AIRFLOW TASKS
# =========================================================

def check_airflow_tasks(dag_id=None):

    if not dag_id:

        return {
            "success": False,
            "tasks": [],
            "error": (
                "No DAG ID was provided."
            )
        }

    result = run_command(
        [
            "airflow",
            "tasks",
            "list",
            dag_id
        ]
    )

    return {
        "success": result["success"],
        "dag_id": dag_id,
        "tasks": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# CHECK AIRFLOW JOBS
# =========================================================

def check_airflow_jobs():

    result = run_command(
        [
            "airflow",
            "jobs",
            "check"
        ]
    )

    return {
        "success": result["success"],
        "output": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# CHECK AIRFLOW CONFIGURATION
# =========================================================

def check_airflow_config():

    result = run_command(
        [
            "airflow",
            "config",
            "get-value",
            "core",
            "dags_folder"
        ]
    )

    return {
        "success": result["success"],
        "dags_folder": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# DETECT DAG ID FROM ERROR
# =========================================================

def extract_dag_id(error_message):

    if not error_message:

        return None

    error_lower = error_message.lower()

    # -----------------------------------------------------
    # Common patterns
    # -----------------------------------------------------

    markers = [
        "dag_id=",
        "dag_id:",
        "dag ",
    ]

    for marker in markers:

        if marker in error_lower:

            index = error_lower.find(marker)

            value = error_message[
                index + len(marker):
            ].strip()

            # Remove common punctuation
            value = (
                value
                .split()[0]
                .strip("'\"`:,.;")
            )

            if value:

                return value

    return None


# =========================================================
# AIRFLOW DEBUGGING TOOL
# =========================================================

def execute_airflow_debugging(
    error_message,
    classification,
    code=None
):

    technology = classification.get(
        "technology",
        ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute for Airflow
    # -----------------------------------------------------

    if technology != "airflow":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "Airflow debugging tool "
                "was not selected."
            )
        }

    # -----------------------------------------------------
    # Initial evidence
    # -----------------------------------------------------

    operating_system = platform.system()

    evidence = {
        "technology": "airflow",
        "tool_executed": True,
        "error_message": error_message,
        "operating_system": operating_system,
        "user_code": code or "No Airflow code provided."
    }

    # -----------------------------------------------------
    # Airflow installation
    # -----------------------------------------------------

    installation = (
        check_airflow_installation()
    )

    evidence["installation"] = installation

    # -----------------------------------------------------
    # Stop early if Airflow is not installed
    # -----------------------------------------------------

    if not installation["installed"]:

        evidence["diagnosis"] = {
            "airflow_installed": False,
            "message": (
                "Airflow is not available in "
                "the current Python environment."
            )
        }

        return evidence

    # -----------------------------------------------------
    # Airflow version
    # -----------------------------------------------------

    evidence["version"] = (
        check_airflow_version()
    )

    # -----------------------------------------------------
    # DAG list
    # -----------------------------------------------------

    evidence["dags"] = (
        check_airflow_dags()
    )

    # -----------------------------------------------------
    # DAG import errors
    # -----------------------------------------------------

    evidence["import_errors"] = (
        check_dag_import_errors()
    )

    # -----------------------------------------------------
    # DAG configuration
    # -----------------------------------------------------

    evidence["configuration"] = (
        check_airflow_config()
    )

    # -----------------------------------------------------
    # Detect DAG ID
    # -----------------------------------------------------

    dag_id = extract_dag_id(
        error_message
    )

    if dag_id:

        evidence["dag_id"] = dag_id

        evidence["tasks"] = (
            check_airflow_tasks(
                dag_id
            )
        )

    else:

        evidence["dag_id"] = None

        evidence["tasks"] = {
            "success": False,
            "tasks": [],
            "error": (
                "DAG ID could not be detected "
                "from the error message."
            )
        }

    # -----------------------------------------------------
    # Check Airflow jobs
    # -----------------------------------------------------

    evidence["jobs"] = (
        check_airflow_jobs()
    )

    # =====================================================
    # DIAGNOSIS
    # =====================================================

    import_errors = evidence[
        "import_errors"
    ]

    jobs = evidence[
        "jobs"
    ]

    dags = evidence[
        "dags"
    ]

    diagnosis = []

    # -----------------------------------------------------
    # Import errors
    # -----------------------------------------------------

    if (
        import_errors["success"]
        and import_errors["import_errors"]
    ):

        diagnosis.append(
            "Airflow has DAG import errors."
        )

    # -----------------------------------------------------
    # DAG listing
    # -----------------------------------------------------

    if not dags["success"]:

        diagnosis.append(
            "Airflow could not list DAGs."
        )

    # -----------------------------------------------------
    # Jobs
    # -----------------------------------------------------

    if not jobs["success"]:

        diagnosis.append(
            "Airflow job health check failed."
        )

    # -----------------------------------------------------
    # No detected issue
    # -----------------------------------------------------

    if not diagnosis:

        diagnosis.append(
            "No immediate Airflow issue was "
            "detected by the available checks."
        )

    evidence["diagnosis"] = {
        "airflow_installed": True,
        "issues": diagnosis
    }

    # -----------------------------------------------------
    # Environment guidance
    # -----------------------------------------------------

    if operating_system == "Windows":

        evidence["environment_guidance"] = (
            "Airflow is being inspected from Windows. "
            "If Airflow is running through Docker, "
            "inspect the Docker containers and Airflow "
            "services rather than assuming a native "
            "Linux systemd service."
        )

    elif operating_system == "Linux":

        evidence["environment_guidance"] = (
            "Airflow is running or being inspected "
            "from Linux."
        )

    elif operating_system == "Darwin":

        evidence["environment_guidance"] = (
            "Airflow is being inspected from macOS."
        )

    else:

        evidence["environment_guidance"] = (
            "Operating system is not recognized."
        )

    return evidence
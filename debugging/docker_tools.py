import platform
import subprocess
import shutil


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
# CHECK DOCKER INSTALLATION
# =========================================================

def check_docker_installation():

    docker_path = shutil.which("docker")

    if not docker_path:

        return {
            "installed": False,
            "docker_path": None,
            "message": (
                "Docker executable was not found "
                "in the system PATH."
            )
        }

    version = run_command(
        ["docker", "--version"]
    )

    return {
        "installed": True,
        "docker_path": docker_path,
        "version": version
    }


# =========================================================
# CHECK DOCKER DAEMON
# =========================================================

def check_docker_daemon():

    result = run_command(
        ["docker", "info"]
    )

    return {
        "running": result["success"],
        "stdout": result["stdout"],
        "stderr": result["stderr"]
    }


# =========================================================
# CHECK DOCKER CONTEXT
# =========================================================

def check_docker_context():

    result = run_command(
        ["docker", "context", "show"]
    )

    return {
        "success": result["success"],
        "context": result["stdout"],
        "error": result["stderr"]
    }


# =========================================================
# CHECK DOCKER CONTAINERS
# =========================================================

def check_docker_containers():

    result = run_command(
        [
            "docker",
            "ps",
            "-a",
            "--format",
            "{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}"
        ]
    )

    containers = []

    if result["success"] and result["stdout"]:

        for line in result["stdout"].splitlines():

            parts = line.split("|")

            if len(parts) == 4:

                containers.append({
                    "id": parts[0],
                    "name": parts[1],
                    "status": parts[2],
                    "image": parts[3]
                })

    return {
        "success": result["success"],
        "containers": containers,
        "error": result["stderr"]
    }


# =========================================================
# CHECK DOCKER IMAGES
# =========================================================

def check_docker_images():

    result = run_command(
        [
            "docker",
            "images",
            "--format",
            "{{.Repository}}|{{.Tag}}|{{.Size}}"
        ]
    )

    images = []

    if result["success"] and result["stdout"]:

        for line in result["stdout"].splitlines():

            parts = line.split("|")

            if len(parts) == 3:

                images.append({
                    "repository": parts[0],
                    "tag": parts[1],
                    "size": parts[2]
                })

    return {
        "success": result["success"],
        "images": images,
        "error": result["stderr"]
    }


# =========================================================
# DOCKER DEBUGGING TOOL
# =========================================================

def execute_docker_debugging(
    error_message,
    classification,
    code=None
):

    technology = classification.get(
        "technology",
        ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute for Docker
    # -----------------------------------------------------

    if technology != "docker":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "Docker debugging tool "
                "was not selected."
            )
        }

    # -----------------------------------------------------
    # Detect operating system
    # -----------------------------------------------------

    operating_system = platform.system()

    # -----------------------------------------------------
    # Initial evidence
    # -----------------------------------------------------

    evidence = {
        "technology": "docker",
        "tool_executed": True,
        "error_message": error_message,
        "operating_system": operating_system,
        "user_code": code or "No Docker code provided."
    }

    # -----------------------------------------------------
    # Docker installation
    # -----------------------------------------------------

    evidence["installation"] = (
        check_docker_installation()
    )

    # -----------------------------------------------------
    # Docker context
    # -----------------------------------------------------

    evidence["context"] = (
        check_docker_context()
    )

    # -----------------------------------------------------
    # Docker daemon
    # -----------------------------------------------------

    evidence["daemon"] = (
        check_docker_daemon()
    )

    # -----------------------------------------------------
    # Containers
    # -----------------------------------------------------

    evidence["containers"] = (
        check_docker_containers()
    )

    # -----------------------------------------------------
    # Images
    # -----------------------------------------------------

    evidence["images"] = (
        check_docker_images()
    )

    # -----------------------------------------------------
    # Environment-specific guidance
    # -----------------------------------------------------

    if operating_system == "Windows":

        evidence["environment_guidance"] = (
            "Docker is running on Windows. "
            "Use Docker Desktop to manage the Docker "
            "daemon. Do not use Linux systemctl commands."
        )

    elif operating_system == "Linux":

        evidence["environment_guidance"] = (
            "Docker is running on Linux. "
            "Docker service commands may be available."
        )

    elif operating_system == "Darwin":

        evidence["environment_guidance"] = (
            "Docker is running on macOS. "
            "Use Docker Desktop to manage the daemon."
        )

    else:

        evidence["environment_guidance"] = (
            "Operating system is not recognized."
        )

    # -----------------------------------------------------
    # Return evidence
    # -----------------------------------------------------

    return evidence
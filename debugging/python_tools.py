import importlib.util
import sys


def check_python_environment():

    return {
        "python_version": sys.version,
        "python_executable": sys.executable
    }


def check_package(package_name):

    installed = (
        importlib.util.find_spec(package_name)
        is not None
    )

    return {
        "package": package_name,
        "installed": installed
    }


def check_import(package_name):

    try:

        module = __import__(package_name)

        return {
            "success": True,
            "package": package_name,
            "version": getattr(
                module,
                "__version__",
                "Unknown"
            )
        }

    except Exception as e:

        return {
            "success": False,
            "package": package_name,
            "error": str(e)
        }
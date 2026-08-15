# =========================================================
# DEBUGGING TOOL ROUTER
# =========================================================

def route_debugging_tool(classification):

    technology = classification.get(
        "technology",
        ""
    ).strip().lower()

    # -----------------------------------------------------
    # Python
    # -----------------------------------------------------

    if technology == "python":

        return {
            "technology": "python",
            "tool": "execute_python_debugging",
            "reason": "Python error detected."
        }

    # -----------------------------------------------------
    # SQL
    # -----------------------------------------------------

    elif technology == "sql":

        return {
            "technology": "sql",
            "tool": "execute_sql_debugging",
            "reason": "SQL error detected."
        }

    # -----------------------------------------------------
    # PostgreSQL
    # -----------------------------------------------------

    elif technology == "postgresql":

        return {
            "technology": "postgresql",
            "tool": "execute_postgresql_tool",
            "reason": "PostgreSQL error detected."
        }

    # -----------------------------------------------------
    # Docker
    # -----------------------------------------------------

    elif technology == "docker":

        return {
            "technology": "docker",
            "tool": "execute_docker_debugging",
            "reason": "Docker error detected."
        }

    # -----------------------------------------------------
    # Airflow
    # -----------------------------------------------------

    elif technology == "airflow":

        return {
            "technology": "airflow",
            "tool": "execute_airflow_debugging",
            "reason": "Airflow error detected."
        }

    # -----------------------------------------------------
    # Unknown
    # -----------------------------------------------------

    return {
        "technology": technology or "unknown",
        "tool": "general_debugging",
        "reason": "No specialized debugging tool was selected."
    }
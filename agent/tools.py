from rag.retriever import get_retriever

from debugging.error_classifier import classify_error
from debugging.code_analyzer import analyze_code
from debugging.solution_generator import generate_solution
from debugging.verifier import verify_solution
from debugging.tool_router import route_debugging_tool

from debugging.python_tools import (
    check_python_environment,
    check_package,
    check_import,
)

from debugging.sql_tools import (
    analyze_sql_error,
)

from debugging.postgresql_tools import (
    execute_postgresql_debugging,
)

from debugging.docker_tools import (
    execute_docker_debugging,
)

from debugging.airflow_tools import (
    execute_airflow_debugging,
)


# =========================================================
# ERROR CLASSIFIER TOOL
# =========================================================

def classification_tool(error_message):
    """
    Classify the user's debugging problem.
    """

    return classify_error(
        error_message
    )


# =========================================================
# CODE ANALYZER TOOL
# =========================================================

def analysis_tool(
    error_message,
    classification,
    code=None,
):
    """
    Analyze the user's code together with
    the classified error.
    """

    return analyze_code(
        error_message=error_message,
        classification=classification,
        code=code,
    )


# =========================================================
# KNOWLEDGE RETRIEVAL TOOL
# =========================================================

def knowledge_search_tool(
    error_message,
    classification,
):
    """
    Retrieve relevant debugging knowledge
    from ChromaDB.
    """

    retriever = get_retriever()

    technology = (
        classification.get(
            "technology",
            ""
        )
        or ""
    ).strip()

    error_type = (
        classification.get(
            "error_type",
            ""
        )
        or ""
    ).strip()

    category = (
        classification.get(
            "category",
            ""
        )
        or ""
    ).strip()

    query = f"""
Technology: {technology}

Error Type: {error_type}

Category: {category}

Error:
{error_message}
"""

    print("\n" + "=" * 60)
    print("RAG KNOWLEDGE SEARCH")
    print("=" * 60)

    print(query)

    try:

        results = retriever.invoke(
            query
        )

    except Exception as e:

        print(
            f"RAG retrieval failed: {e}"
        )

        return (
            "No knowledge could be retrieved.",
            []
        )

    # -----------------------------------------------------
    # Build knowledge context
    # -----------------------------------------------------

    knowledge_parts = []

    documents = []

    for result in results:

        page_content = getattr(
            result,
            "page_content",
            ""
        )

        metadata = getattr(
            result,
            "metadata",
            {}
        )

        if page_content:

            knowledge_parts.append(
                page_content
            )

        documents.append(
            {
                "content": page_content,
                "metadata": metadata,
            }
        )

    knowledge = "\n\n".join(
        knowledge_parts
    )

    print(
        f"Retrieved {len(results)} documents."
    )

    return (
        knowledge,
        documents
    )


# =========================================================
# SOLUTION GENERATOR TOOL
# =========================================================

def solution_tool(
    error_message,
    classification,
    analysis,
    knowledge,
    code=None,
    tool_result=None,
    previous_verification=None,
):
    """
    Generate an evidence-based debugging solution.

    IMPORTANT:
    previous_verification is passed to the Solution Agent
    during retry attempts.

    This allows the Solution Agent to learn from the
    Verification Agent's rejection.
    """

    return generate_solution(
        error_message=error_message,
        classification=classification,
        analysis=analysis,
        knowledge=knowledge,
        code=code,
        tool_result=tool_result,
        previous_verification=previous_verification,
    )


# =========================================================
# VERIFICATION TOOL
# =========================================================

def verification_tool(
    error_message,
    classification,
    analysis,
    solution,
    code=None,
    tool_result=None,
):
    """
    Verify whether the generated solution is
    technically correct.

    The original debugging tool result is also passed
    to the verifier so that it can detect contradictions.
    """

    return verify_solution(
        error_message=error_message,
        classification=classification,
        analysis=analysis,
        solution=solution,
        code=code,
        tool_result=tool_result,
    )


# =========================================================
# PYTHON DEBUGGING TOOLS
# =========================================================

def python_environment_tool():
    """
    Check the current Python environment.
    """

    return check_python_environment()


def python_package_tool(
    package_name
):
    """
    Check whether a Python package is installed.
    """

    return check_package(
        package_name
    )


def python_import_tool(
    package_name
):
    """
    Check whether a Python package can be imported.
    """

    return check_import(
        package_name
    )


# =========================================================
# PYTHON DEBUGGING EXECUTION TOOL
# =========================================================

def execute_python_debugging(
    error_message,
    classification,
):
    """
    Execute Python-specific debugging checks.
    """

    technology = (
        classification.get(
            "technology",
            ""
        )
        or ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute Python tools for Python errors
    # -----------------------------------------------------

    if technology != "python":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "Python debugging tool "
                "was not selected."
            ),
        }

    # -----------------------------------------------------
    # Base evidence
    # -----------------------------------------------------

    evidence = {
        "technology": "python",
        "tool_executed": True,
        "error_message": error_message,
    }

    # -----------------------------------------------------
    # Check Python environment
    # -----------------------------------------------------

    try:

        environment = (
            python_environment_tool()
        )

        evidence["environment"] = (
            environment
        )

    except Exception as e:

        evidence["environment"] = {
            "status": "error",
            "error": str(e),
        }

    # -----------------------------------------------------
    # Detect missing package
    # -----------------------------------------------------

    if (
        "No module named"
        in error_message
    ):

        package = (
            error_message
            .split(
                "No module named"
            )[-1]
            .strip()
            .strip("'")
            .strip('"')
        )

        # -------------------------------------------------
        # Handle submodules
        # -------------------------------------------------

        package_root = (
            package.split(".")[0]
        )

        evidence["package_name"] = (
            package_root
        )

        # -------------------------------------------------
        # Check package installation
        # -------------------------------------------------

        try:

            evidence["package"] = (
                python_package_tool(
                    package_root
                )
            )

        except Exception as e:

            evidence["package"] = {
                "status": "error",
                "error": str(e),
            }

        # -------------------------------------------------
        # Check import
        # -------------------------------------------------

        try:

            evidence["import"] = (
                python_import_tool(
                    package_root
                )
            )

        except Exception as e:

            evidence["import"] = {
                "status": "error",
                "error": str(e),
            }

    return evidence


# =========================================================
# SQL DEBUGGING EXECUTION TOOL
# =========================================================

def execute_sql_debugging(
    error_message,
    classification,
    code=None,
):
    """
    Execute SQL-specific debugging.
    """

    technology = (
        classification.get(
            "technology",
            ""
        )
        or ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute SQL tool for SQL errors
    # -----------------------------------------------------

    if technology != "sql":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "SQL debugging tool "
                "was not selected."
            ),
        }

    try:

        result = analyze_sql_error(
            error_message=error_message,
            sql_query=code,
        )

        result["tool_executed"] = True

        result["tool_name"] = (
            "execute_sql_debugging"
        )

        return result

    except Exception as e:

        return {
            "technology": technology,
            "tool_executed": False,
            "tool_name": (
                "execute_sql_debugging"
            ),
            "error": str(e),
        }


# =========================================================
# POSTGRESQL DEBUGGING EXECUTION TOOL
# =========================================================

def execute_postgresql_tool(
    error_message,
    classification,
    code=None,
):
    """
    Execute PostgreSQL-specific debugging.
    """

    technology = (
        classification.get(
            "technology",
            ""
        )
        or ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute PostgreSQL tool for PostgreSQL errors
    # -----------------------------------------------------

    if technology != "postgresql":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "PostgreSQL debugging tool "
                "was not selected."
            ),
        }

    try:

        result = execute_postgresql_debugging(
            error_message=error_message,
            classification=classification,
            code=code,
        )

        result["tool_executed"] = True

        result["tool_name"] = (
            "execute_postgresql_tool"
        )

        return result

    except Exception as e:

        return {
            "technology": technology,
            "tool_executed": False,
            "tool_name": (
                "execute_postgresql_tool"
            ),
            "error": str(e),
        }


# =========================================================
# DOCKER DEBUGGING EXECUTION TOOL
# =========================================================

def execute_docker_tool(
    error_message,
    classification,
    code=None,
):
    """
    Execute Docker-specific debugging.
    """

    technology = (
        classification.get(
            "technology",
            ""
        )
        or ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute Docker tool for Docker errors
    # -----------------------------------------------------

    if technology != "docker":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "Docker debugging tool "
                "was not selected."
            ),
        }

    try:

        result = execute_docker_debugging(
            error_message=error_message,
            classification=classification,
            code=code,
        )

        result["tool_executed"] = True

        result["tool_name"] = (
            "execute_docker_debugging"
        )

        return result

    except Exception as e:

        return {
            "technology": technology,
            "tool_executed": False,
            "tool_name": (
                "execute_docker_debugging"
            ),
            "error": str(e),
        }


# =========================================================
# AIRFLOW DEBUGGING EXECUTION TOOL
# =========================================================

def execute_airflow_tool(
    error_message,
    classification,
    code=None,
):
    """
    Execute Airflow-specific debugging.
    """

    technology = (
        classification.get(
            "technology",
            ""
        )
        or ""
    ).strip().lower()

    # -----------------------------------------------------
    # Only execute Airflow tools for Airflow errors
    # -----------------------------------------------------

    if technology != "airflow":

        return {
            "technology": technology,
            "tool_executed": False,
            "message": (
                "Airflow debugging tool "
                "was not selected."
            ),
        }

    try:

        result = execute_airflow_debugging(
            error_message=error_message,
            classification=classification,
            code=code,
        )

        result["tool_executed"] = True

        result["tool_name"] = (
            "execute_airflow_debugging"
        )

        return result

    except Exception as e:

        return {
            "technology": technology,
            "tool_executed": False,
            "tool_name": (
                "execute_airflow_debugging"
            ),
            "error": str(e),
        }


# =========================================================
# DEBUGGING TOOL ROUTER
# =========================================================

def debugging_tool_router(
    classification,
):
    """
    Decide which debugging tool should be executed
    based on the classification.
    """

    return route_debugging_tool(
        classification
    )
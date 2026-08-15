from typing import Dict, Any


# ============================================================
# POSTGRESQL INDICATORS
# ============================================================

POSTGRESQL_KEYWORDS = [
    "postgresql",
    "postgres",
    "psql",
    "pgadmin",
    "psycopg",
    "psycopg2",
    "asyncpg",
    "postgresql+",
    "postgres://",
    "postgresql://",

    # PostgreSQL error types
    "undefinedcolumn",
    "undefinedtable",
    "undefined_column",
    "undefined_table",
    "duplicatekey",
    "duplicate_key",
    "foreignkeyviolation",
    "foreign_key_violation",
    "datatype_mismatch",
    "relation does not exist",
    "column does not exist",

    # PostgreSQL-specific connection/configuration
    "password authentication failed",
    "could not connect to server",
    "connection refused",
    "database does not exist",
    "no pg_hba.conf entry",
    "operator does not exist",
]


# ============================================================
# GENERAL TECHNOLOGY KEYWORDS
# ============================================================

PYTHON_KEYWORDS = [
    "python",
    "traceback",
    "modulenotfounderror",
    "importerror",
    "nameerror",
    "typeerror",
    "attributeerror",
    "keyerror",
]

DOCKER_KEYWORDS = [
    "docker",
    "docker daemon",
    "dockerfile",
    "docker compose",
    "container",
    "image not found",
    "port is already allocated",
]

AIRFLOW_KEYWORDS = [
    "airflow",
    "broken dag",
    "dag import",
    "scheduler",
    "airflow task",
    "airflow operator",
]


# ============================================================
# HELPER
# ============================================================

def contains_keyword(
    text: str,
    keywords: list[str]
) -> bool:

    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


# ============================================================
# SUPERVISOR AGENT
# ============================================================

def supervisor_agent(
    state: Dict[str, Any]
):
    """
    Supervisor Agent

    Determines which specialized debugging
    agent should handle the problem.

    Routing priority:

    1. Explicit PostgreSQL evidence
    2. Explicit Python evidence
    3. Explicit Docker evidence
    4. Explicit Airflow evidence
    5. Classifier technology
    6. Generic SQL fallback
    """

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    classification = state.get(
        "classification",
        {}
    )

    technology = (
        classification
        .get("technology", "")
        .lower()
        .strip()
    )

    category = (
        classification
        .get("category", "")
        .lower()
        .strip()
    )

    error_type = (
        classification
        .get("error_type", "")
        .lower()
        .strip()
    )

    error_message = (
        state.get(
            "error_message",
            ""
        )
    )

    code = (
        state.get(
            "code",
            ""
        )
    )

    # --------------------------------------------------------
    # Combine available evidence
    # --------------------------------------------------------

    evidence = " ".join([
        technology,
        category,
        error_type,
        error_message,
        code
    ]).lower()

    # ========================================================
    # ROUTING
    # ========================================================

    selected_agent = "general_debugging_agent"

    routing_reason = (
        "Unable to determine a specialized "
        "debugging technology."
    )

    # ========================================================
    # 1. POSTGRESQL
    # ========================================================

    if contains_keyword(
        evidence,
        POSTGRESQL_KEYWORDS
    ):

        selected_agent = "postgresql_agent"

        routing_reason = (
            "PostgreSQL-specific evidence "
            "was detected in the classification, "
            "error message, or code."
        )

    # ========================================================
    # 2. PYTHON
    # ========================================================

    elif contains_keyword(
        evidence,
        PYTHON_KEYWORDS
    ):

        selected_agent = "python_agent"

        routing_reason = (
            "Python-specific error or "
            "environment evidence was detected."
        )

    # ========================================================
    # 3. DOCKER
    # ========================================================

    elif contains_keyword(
        evidence,
        DOCKER_KEYWORDS
    ):

        selected_agent = "docker_agent"

        routing_reason = (
            "Docker-specific error or "
            "container evidence was detected."
        )

    # ========================================================
    # 4. AIRFLOW
    # ========================================================

    elif contains_keyword(
        evidence,
        AIRFLOW_KEYWORDS
    ):

        selected_agent = "airflow_agent"

        routing_reason = (
            "Airflow-specific error or "
            "DAG/scheduler evidence was detected."
        )

    # ========================================================
    # 5. CLASSIFICATION-BASED ROUTING
    # ========================================================

    else:

        routing = {

            "python":
                "python_agent",

            "sql":
                "sql_agent",

            "postgresql":
                "postgresql_agent",

            "docker":
                "docker_agent",

            "airflow":
                "airflow_agent",
        }

        selected_agent = routing.get(
            technology,
            "general_debugging_agent"
        )

        routing_reason = (
            f"The problem was classified as "
            f"{technology or 'unknown'}"
        )

        if category:

            routing_reason += (
                f" / {category}"
            )

        if error_type:

            routing_reason += (
                f" / {error_type}"
            )

    # ========================================================
    # LOGGING
    # ========================================================

    print("\n" + "=" * 60)
    print("SUPERVISOR AGENT")
    print("=" * 60)

    print(
        f"Detected Technology : "
        f"{technology or 'unknown'}"
    )

    print(
        f"Detected Category   : "
        f"{category or 'unknown'}"
    )

    print(
        f"Detected Error Type : "
        f"{error_type or 'unknown'}"
    )

    print(
        f"Selected Agent      : "
        f"{selected_agent}"
    )

    print(
        f"Routing Reason      : "
        f"{routing_reason}"
    )

    print("=" * 60)

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "selected_agent": selected_agent,
        "routing_reason": routing_reason
    }
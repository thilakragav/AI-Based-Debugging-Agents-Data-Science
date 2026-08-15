from typing import Dict, Any

from debugging.postgresql_tools import (
    execute_postgresql_debugging
)


def postgresql_agent(state: Dict[str, Any]):
    """
    PostgreSQL Specialist Agent.

    Performs PostgreSQL-specific debugging using:
    - PostgreSQL connection validation
    - Table validation
    - Column validation
    - Schema inspection
    - Missing-column discovery
    - JOIN analysis
    - Corrected SQL generation
    """

    error_message = state.get(
        "error_message",
        ""
    )

    code = state.get(
        "code",
        ""
    )

    rag_context = state.get(
        "rag_context",
        ""
    )

    classification = state.get(
        "classification",
        {}
    )

    error_type = classification.get(
        "error_type",
        "Unknown"
    )

    # =====================================================
    # BASIC POSTGRESQL ANALYSIS
    # =====================================================

    analysis = {
        "technology": "postgresql",
        "error_type": error_type,
        "error": error_message,
        "code": code,
        "rag_context": rag_context,
        "checks": [
            "Verify the PostgreSQL table exists.",
            "Verify the referenced column exists.",
            "Verify the table alias.",
            "Verify the schema.",
            "Check whether a JOIN is required."
        ]
    }

    # =====================================================
    # EXECUTE POSTGRESQL DEBUGGING TOOLS
    # =====================================================

    try:

        debugging_result = execute_postgresql_debugging(
            error_message=error_message,
            classification=classification,
            code=code
        )

        # Add the actual PostgreSQL investigation
        analysis["postgresql_debugging"] = (
            debugging_result
        )

        # =================================================
        # ADD DISCOVERED INFORMATION
        # =================================================

        if debugging_result.get(
            "connection"
        ):
            analysis["connection"] = (
                debugging_result["connection"]
            )

        if debugging_result.get(
            "table"
        ):
            analysis["table"] = (
                debugging_result["table"]
            )

        if debugging_result.get(
            "column"
        ):
            analysis["column"] = (
                debugging_result["column"]
            )

        if debugging_result.get(
            "schema"
        ):
            analysis["schema"] = (
                debugging_result["schema"]
            )

        if debugging_result.get(
            "column_search"
        ):
            analysis["column_search"] = (
                debugging_result["column_search"]
            )

        if debugging_result.get(
            "join_analysis"
        ):
            analysis["join_analysis"] = (
                debugging_result["join_analysis"]
            )

        # =================================================
        # CORRECTED SQL
        # =================================================

        if debugging_result.get(
            "corrected_sql"
        ):

            analysis["corrected_sql"] = (
                debugging_result["corrected_sql"]
            )

        # =================================================
        # EVIDENCE
        # =================================================

        if debugging_result.get(
            "evidence"
        ):

            analysis["evidence"] = (
                debugging_result["evidence"]
            )

    except Exception as e:

        analysis["postgresql_debugging_error"] = (
            str(e)
        )

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {
        "technology_analysis": analysis
    }
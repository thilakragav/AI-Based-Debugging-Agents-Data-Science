import re


# =========================================================
# SQL ERROR ANALYSIS
# =========================================================

def analyze_sql_error(error_message, sql_query=None):

    error_lower = error_message.lower()

    result = {
        "technology": "sql",
        "tool_executed": True,
        "error_type": "Unknown",
        "category": "Unknown",
        "evidence": [],
        "sql_query": sql_query or "",
    }

    # -----------------------------------------------------
    # Syntax Error
    # -----------------------------------------------------

    if (
        "syntax error" in error_lower
        or "sql syntax" in error_lower
        or "near" in error_lower
    ):

        result["error_type"] = "SyntaxError"
        result["category"] = "SQL Syntax"

        result["evidence"].append(
            "The database reported a SQL syntax-related error."
        )

    # -----------------------------------------------------
    # Missing Table
    # -----------------------------------------------------

    elif (
        "table" in error_lower
        and (
            "does not exist" in error_lower
            or "not found" in error_lower
        )
    ):

        result["error_type"] = "TableNotFound"
        result["category"] = "Schema"

        result["evidence"].append(
            "The referenced table may not exist."
        )

    # -----------------------------------------------------
    # Missing Column
    # -----------------------------------------------------

    elif (
        "column" in error_lower
        and (
            "does not exist" in error_lower
            or "not found" in error_lower
            or "unknown column" in error_lower
        )
    ):

        result["error_type"] = "ColumnNotFound"
        result["category"] = "Schema"

        result["evidence"].append(
            "The query references a column that may not exist."
        )

    # -----------------------------------------------------
    # Ambiguous Column
    # -----------------------------------------------------

    elif "ambiguous" in error_lower:

        result["error_type"] = "AmbiguousColumn"
        result["category"] = "SQL Query"

        result["evidence"].append(
            "A column reference is ambiguous."
        )

    # -----------------------------------------------------
    # GROUP BY Error
    # -----------------------------------------------------

    elif (
        "group by" in error_lower
        or "not in group by" in error_lower
    ):

        result["error_type"] = "GroupByError"
        result["category"] = "Aggregation"

        result["evidence"].append(
            "The query may contain an invalid GROUP BY expression."
        )

    # -----------------------------------------------------
    # JOIN Error
    # -----------------------------------------------------

    elif (
        "join" in error_lower
        or "foreign key" in error_lower
    ):

        result["error_type"] = "JoinError"
        result["category"] = "Join"

        result["evidence"].append(
            "The query may contain an invalid JOIN condition."
        )

    # -----------------------------------------------------
    # Default
    # -----------------------------------------------------

    else:

        result["evidence"].append(
            "No specific SQL error pattern was detected."
        )

    # -----------------------------------------------------
    # Extract possible table / column information
    # -----------------------------------------------------

    result["referenced_tables"] = []

    result["referenced_columns"] = []

    if sql_query:

        table_matches = re.findall(
            r"\b(?:FROM|JOIN)\s+([a-zA-Z_][\w.]*)",
            sql_query,
            flags=re.IGNORECASE,
        )

        result["referenced_tables"] = list(
            dict.fromkeys(table_matches)
        )

    return result
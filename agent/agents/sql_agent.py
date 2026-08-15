def sql_agent(state):

    error_message = state.get("error_message", "")
    code = state.get("code", "")
    rag_context = state.get("rag_context", "")

    return {
        "specialist_analysis": {
            "technology": "sql",
            "error": error_message,
            "code": code,
            "rag_context": rag_context,
            "checks": [
                "Check SQL syntax.",
                "Check table names.",
                "Check column names.",
                "Check joins.",
                "Check aggregation.",
                "Check aliases."
            ]
        }
    }
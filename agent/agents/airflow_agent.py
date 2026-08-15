def airflow_agent(state):

    error_message = state.get("error_message", "")
    code = state.get("code", "")
    rag_context = state.get("rag_context", "")

    return {
        "specialist_analysis": {
            "technology": "airflow",
            "error": error_message,
            "code": code,
            "rag_context": rag_context,
            "checks": [
                "Check DAG syntax.",
                "Check DAG imports.",
                "Check scheduler.",
                "Check task logs.",
                "Check Airflow connections.",
                "Check operator configuration."
            ]
        }
    }
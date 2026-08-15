def python_agent(state):

    error_message = state.get("error_message", "")
    code = state.get("code", "")
    rag_context = state.get("rag_context", "")

    return {
        "specialist_analysis": {
            "technology": "python",
            "error": error_message,
            "code": code,
            "rag_context": rag_context,
            "checks": [
                "Check Python syntax.",
                "Check imports.",
                "Check installed packages.",
                "Check virtual environment.",
                "Check Python version."
            ]
        }
    }
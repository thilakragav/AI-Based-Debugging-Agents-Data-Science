def docker_agent(state):

    error_message = state.get("error_message", "")
    code = state.get("code", "")
    rag_context = state.get("rag_context", "")

    return {
        "specialist_analysis": {
            "technology": "docker",
            "error": error_message,
            "code": code,
            "rag_context": rag_context,
            "checks": [
                "Check Docker daemon.",
                "Check Docker context.",
                "Check container status.",
                "Check container logs.",
                "Check port mapping.",
                "Check Docker networking."
            ]
        }
    }
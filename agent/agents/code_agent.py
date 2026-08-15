from debugging.code_analyzer import analyze_code


def code_agent(state):

    result = analyze_code(
        error_message=state["error_message"],
        code=state.get("code"),
        classification=state.get("classification")
    )

    return {
        "code_analysis": result
    }
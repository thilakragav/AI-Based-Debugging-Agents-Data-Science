from debugging.error_classifier import classify_error


def error_agent(state):

    error_message = state["error_message"]

    classification = classify_error(
        error_message
    )

    return {
        "classification": classification
    }
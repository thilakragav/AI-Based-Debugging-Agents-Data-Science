from typing import Dict, Any

from agent.tools import verification_tool


def verification_agent(state: Dict[str, Any]):
    """
    Verification Agent.

    Checks whether the generated solution is
    technically correct using:

    - original error
    - classification
    - analysis
    - generated solution
    - original code
    - debugging tool evidence
    """

    error_message = state.get(
        "error_message",
        ""
    )

    classification = state.get(
        "classification",
        {}
    )

    analysis = state.get(
        "analysis",
        {}
    )

    solution = state.get(
        "solution",
        {}
    )

    code = state.get(
        "code",
        ""
    )

    tool_result = state.get(
        "tool_result",
        {}
    )

    print("\n" + "=" * 60)
    print("VERIFICATION AGENT")
    print("=" * 60)

    print(
        "Verifying generated solution..."
    )

    # ---------------------------------------------------------
    # Execute existing verification tool
    # ---------------------------------------------------------

    verification = verification_tool(
        error_message=error_message,
        classification=classification,
        analysis=analysis,
        solution=solution,
        code=code,
        tool_result=tool_result
    )

    print(
        "Verification Agent completed."
    )

    print(
        f"Verification Status : "
        f"{verification.get('status', 'UNKNOWN')}"
    )

    print("=" * 60)

    return {
        "verification": verification
    }
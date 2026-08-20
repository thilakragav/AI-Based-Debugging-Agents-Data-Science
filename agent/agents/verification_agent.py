from typing import Dict, Any

from agent.tools import (
    verification_tool,
    corrected_code_execution_tool,
)


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
    # Technology-aware corrected-code execution
    # ---------------------------------------------------------

    corrected_code = ""

    if isinstance(solution, dict):
        corrected_code = solution.get(
            "corrected_code",
            ""
        )

    # Determine the technology from classification first.
    technology = ""

    if isinstance(classification, dict):
        technology = classification.get(
            "technology",
            ""
        )

    technology = str(technology).strip().lower()

    execution_result = {
        "executed": False,
        "status": "NOT_APPLICABLE",
        "reason": (
            "Automatic Python execution is only used for "
            "Python corrections. Technology-specific tools "
            "handle other technologies."
        ),
        "stdout": "",
        "stderr": "",
        "return_code": None,
    }

    # ---------------------------------------------------------
    # Python-only execution
    # ---------------------------------------------------------

    if technology == "python":

        if corrected_code and corrected_code.strip():

            print("\n" + "-" * 60)
            print("CORRECTED PYTHON CODE EXECUTION")
            print("-" * 60)

            execution_result = corrected_code_execution_tool(
                corrected_code=corrected_code,
                timeout=10,
            )

            print(
                f"Execution Status : "
                f"{execution_result.get('status', 'UNKNOWN')}"
            )

            print(
                f"Execution Reason : "
                f"{execution_result.get('reason', '')}"
            )

        else:

            execution_result = {
                "executed": False,
                "status": "NOT_EXECUTED",
                "reason": "No corrected Python code available.",
                "stdout": "",
                "stderr": "",
                "return_code": None,
            }

    else:

        print("\n" + "-" * 60)
        print("TECHNOLOGY-SPECIFIC EXECUTION")
        print("-" * 60)
        print(
            f"Technology        : {technology or 'unknown'}"
        )
        print(
            "Execution Status  : NOT_APPLICABLE"
        )
        print(
            "Reason            : "
            "Python executor is not used for this technology."
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

    # Attach actual execution evidence.
    verification["execution"] = execution_result

    print(
        "Verification Agent completed."
    )

    print(
        f"Verification Status : "
        f"{verification.get('status', 'UNKNOWN')}"
    )

    print(
        f"Execution Status : "
        f"{execution_result.get('status', 'UNKNOWN')}"
    )

    print("=" * 60)

    return {
        "verification": verification
    }
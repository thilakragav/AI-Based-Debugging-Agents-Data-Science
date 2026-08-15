from typing import Dict, Any

from agent.tools import solution_tool


def solution_agent(state: Dict[str, Any]):
    """
    Solution Agent.

    Uses:
    - error information
    - classification
    - code analysis
    - RAG knowledge
    - specialist analysis
    - debugging tool evidence
    - previous verification feedback

    to generate an evidence-based debugging solution.
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

    rag_context = state.get(
        "rag_context",
        ""
    )

    specialist_analysis = state.get(
        "specialist_analysis",
        {}
    )

    tool_result = state.get(
        "tool_result",
        {}
    )

    code = state.get(
        "code",
        ""
    )

    previous_verification = state.get(
        "verification",
        {}
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    # ---------------------------------------------------------
    # Build enhanced knowledge
    # ---------------------------------------------------------

    enhanced_knowledge = f"""
==================================================
RAG KNOWLEDGE
==================================================

{rag_context}


==================================================
SPECIALIST ANALYSIS
==================================================

{specialist_analysis}


==================================================
ERROR ANALYSIS
==================================================

{analysis}


==================================================
DEBUGGING TOOL RESULT
==================================================

{tool_result}
"""

    # ---------------------------------------------------------
    # Retry feedback
    # ---------------------------------------------------------

    if retry_count > 0 and previous_verification:

        enhanced_knowledge += f"""

==================================================
PREVIOUS VERIFICATION FEEDBACK
==================================================

The previous solution failed verification.

Verification result:

{previous_verification}

Retry attempt:
{retry_count}

IMPORTANT:

1. Do not blindly repeat the previous solution.
2. Address the verifier's issues.
3. Trust factual debugging-tool evidence.
4. Do not invent database tables or columns.
5. Do not recommend installing packages that are already installed.
6. Produce an improved solution.
"""

    print("\n" + "=" * 60)
    print("SOLUTION AGENT")
    print("=" * 60)

    print(
        f"Retry Count : {retry_count}"
    )

    print(
        "Generating evidence-based solution..."
    )

    # ---------------------------------------------------------
    # Execute existing solution tool
    # ---------------------------------------------------------

    solution = solution_tool(
        error_message=error_message,
        classification=classification,
        analysis=analysis,
        knowledge=enhanced_knowledge,
        code=code,
        tool_result=tool_result,
        previous_verification=previous_verification
    )

    print(
        "Solution Agent completed."
    )

    print("=" * 60)

    return {
        "solution": solution
    }
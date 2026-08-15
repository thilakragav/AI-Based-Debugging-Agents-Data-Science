import json

from debugging.llm import get_llm


# =========================================================
# RESPONSE NORMALIZER
# =========================================================

def normalize_response(response):

    content = response.content

    # LangChain may return a list of content blocks
    if isinstance(content, list):

        text_parts = []

        for block in content:

            if isinstance(block, str):

                text_parts.append(block)

            elif isinstance(block, dict):

                if "text" in block:

                    text_parts.append(
                        str(block["text"])
                    )

        content = "".join(text_parts)

    return str(content).strip()


# =========================================================
# VERIFY SOLUTION
# =========================================================

def verify_solution(
    error_message,
    classification,
    analysis,
    solution,
    code=None,
    tool_result=None
):

    # -----------------------------------------------------
    # Get LLM
    # -----------------------------------------------------

    llm = get_llm()

    # -----------------------------------------------------
    # Convert inputs to JSON/text
    # -----------------------------------------------------

    classification_text = json.dumps(
        classification,
        indent=2,
        default=str
    )

    analysis_text = json.dumps(
        analysis,
        indent=2,
        default=str
    )

    solution_text = json.dumps(
        solution,
        indent=2,
        default=str
    )

    tool_result_text = json.dumps(
        tool_result or {},
        indent=2,
        default=str
    )

    code_text = (
        code
        if code
        else "No code was provided."
    )

    # =====================================================
    # VERIFICATION PROMPT
    # =====================================================

    prompt = f"""
You are a senior software debugging verification agent.

Your job is to determine whether the proposed debugging
solution is actually supported by the available evidence.

You MUST prioritize factual debugging evidence over
assumptions or guesses.

==========================================================
USER ERROR
==========================================================

{error_message}


==========================================================
ERROR CLASSIFICATION
==========================================================

{classification_text}


==========================================================
CODE ANALYSIS
==========================================================

{analysis_text}


==========================================================
DEBUGGING TOOL RESULT
==========================================================

{tool_result_text}


==========================================================
PROPOSED SOLUTION
==========================================================

{solution_text}


==========================================================
USER CODE
==========================================================

{code_text}


==========================================================
VERIFICATION RULES
==========================================================

Evaluate the proposed solution using the following rules.

1. Does the proposed root cause explain the actual error?

2. Is the root cause supported by the debugging
   tool result?

3. Is the root cause supported by the RAG/analysis
   information?

4. Does the proposed solution directly address the
   identified root cause?

5. Does the corrected code or command actually address
   the error?

6. Are the verification steps technically appropriate?

7. Could the proposed solution introduce another problem?

8. Is important information missing?

9. Most importantly:

   NEVER mark a solution PASS if it directly contradicts
   factual evidence from the debugging tool.

10. If the debugging tool says a package, service,
    connection, file, table, column, or configuration
    already exists or works, do not approve a solution
    that assumes it is missing without additional evidence.

11. If the evidence is contradictory or insufficient,
    return FAIL or Medium/Low confidence instead of
    guessing.

==========================================================
IMPORTANT EXAMPLE
==========================================================

If the debugging tool says:

package_installed = true
import_success = true

and the solution says:

"Install the package"

then this is a contradiction.

The correct verification result should be:

status = FAIL

because the proposed solution does not address the
actual evidence.

==========================================================
FINAL DECISION
==========================================================

PASS means:

- Root cause is supported.
- Solution addresses the root cause.
- Solution does not contradict tool evidence.
- Corrected code/command is reasonable.
- Verification steps are sufficient.

FAIL means:

- Root cause is unsupported.
- Solution contradicts tool evidence.
- Solution does not address the actual problem.
- Corrected code is incorrect.
- Important evidence was ignored.

==========================================================
OUTPUT FORMAT
==========================================================

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json.

Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "status": "PASS or FAIL",
    "confidence": "High/Medium/Low",
    "reason": "...",
    "issues": [
        "...",
        "..."
    ],
    "recommended_changes": [
        "...",
        "..."
    ]
}}
"""

    # =====================================================
    # CALL LLM
    # =====================================================

    response = llm.invoke(
        prompt
    )

    # =====================================================
    # NORMALIZE RESPONSE
    # =====================================================

    content = normalize_response(
        response
    )

    # =====================================================
    # REMOVE MARKDOWN FENCES
    # =====================================================

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    # =====================================================
    # EXTRACT JSON OBJECT
    # =====================================================

    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1:

        content = content[
            start:end + 1
        ]

    # =====================================================
    # PARSE JSON
    # =====================================================

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        print("=" * 60)
        print(
            "LLM VERIFIER RETURNED INVALID JSON"
        )
        print("=" * 60)

        print(content)

        raise ValueError(
            "Verifier returned invalid JSON."
        )

    # =====================================================
    # VALIDATE REQUIRED FIELDS
    # =====================================================

    required_fields = [
        "status",
        "confidence",
        "reason",
        "issues",
        "recommended_changes"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:

        raise ValueError(
            "Verifier response is missing fields: "
            + ", ".join(missing_fields)
        )

    # =====================================================
    # NORMALIZE STATUS
    # =====================================================

    status = str(
        result["status"]
    ).strip().upper()

    if status.startswith("PASS"):

        result["status"] = "PASS"

    elif status.startswith("FAIL"):

        result["status"] = "FAIL"

    else:

        # Unknown status = FAIL for safety

        result["status"] = "FAIL"

    # =====================================================
    # NORMALIZE CONFIDENCE
    # =====================================================

    confidence = str(
        result["confidence"]
    ).strip().capitalize()

    if confidence not in (
        "High",
        "Medium",
        "Low"
    ):

        confidence = "Low"

    result["confidence"] = confidence

    # =====================================================
    # ENSURE ISSUES IS A LIST
    # =====================================================

    if not isinstance(
        result["issues"],
        list
    ):

        result["issues"] = [
            str(
                result["issues"]
            )
        ]

    # =====================================================
    # ENSURE RECOMMENDED CHANGES IS A LIST
    # =====================================================

    if not isinstance(
        result["recommended_changes"],
        list
    ):

        result["recommended_changes"] = [
            str(
                result["recommended_changes"]
            )
        ]

    # =====================================================
    # SAFETY CHECK
    # =====================================================

    # If the verifier has no actual tool evidence,
    # don't artificially claim high confidence.

    if not tool_result:

        if result["confidence"] == "High":

            result["confidence"] = "Medium"

    # =====================================================
    # PRINT VERIFICATION SUMMARY
    # =====================================================

    print("\n" + "=" * 60)
    print("VERIFICATION AGENT")
    print("=" * 60)

    print(
        "Status:",
        result["status"]
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "Reason:",
        result["reason"]
    )

    if result["issues"]:

        print("\nIssues:")

        for issue in result["issues"]:

            print(
                f"- {issue}"
            )

    if result["recommended_changes"]:

        print("\nRecommended Changes:")

        for change in result[
            "recommended_changes"
        ]:

            print(
                f"- {change}"
            )

    print("=" * 60)

    # =====================================================
    # RETURN
    # =====================================================

    return result
import json
import re

from debugging.llm import get_llm

# Evidence-aware solution schema: CONFIRMED / PROBABLE / UNKNOWN root cause status.


# =========================================================
# RESPONSE NORMALIZER
# =========================================================

def normalize_response(response):
    """
    Normalize LangChain/Groq response content into plain text.
    """

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
# CLEAN JSON RESPONSE
# =========================================================

def clean_json_response(content):
    """
    Remove Markdown fences and extract the JSON object.
    """

    content = str(content).strip()

    # -----------------------------------------------------
    # Remove ```json
    # -----------------------------------------------------

    content = re.sub(
        r"```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    # -----------------------------------------------------
    # Remove ```
    # -----------------------------------------------------

    content = re.sub(
        r"```\s*",
        "",
        content
    )

    content = content.strip()

    # -----------------------------------------------------
    # Extract JSON object
    # -----------------------------------------------------

    start = content.find("{")
    end = content.rfind("}")

    if (
        start != -1
        and end != -1
        and end > start
    ):

        content = content[
            start:end + 1
        ]

    return content.strip()


# =========================================================
# PARSE JSON RESPONSE
# =========================================================

def parse_json_response(content):
    """
    Parse and safely normalize JSON returned by the LLM.

    Handles:
    - Markdown ```json fences
    - Extra text around JSON
    - Invalid backslash escapes such as \\d
    - Normal JSON escape sequences
    """

    cleaned = clean_json_response(
        content
    )

    # -----------------------------------------------------
    # Fix invalid JSON backslash escapes
    # -----------------------------------------------------
    #
    # JSON only permits these escapes:
    #   \" \\ \/ \b \f \n \r \t \uXXXX
    #
    # PostgreSQL commands such as:
    #   \d customers
    #
    # are not valid JSON escapes. Convert unknown escapes
    # such as \d into \\d before json.loads().
    # -----------------------------------------------------

    def _fix_invalid_json_escapes(match):
        """
        JSON requires an even number of backslashes before a
        character that is not a valid JSON escape. If the LLM
        returns an odd-length run such as \\d or \\\d, add one
        backslash so the resulting JSON is valid.
        """
        slashes = match.group(0)

        if len(slashes) % 2 == 1:
            return slashes + "\\"

        return slashes

    cleaned = re.sub(
        r'\\+(?=[^"\\/bfnrtu0-9])',
        _fix_invalid_json_escapes,
        cleaned
    )

    try:

        result = json.loads(
            cleaned
        )

    except json.JSONDecodeError as e:

        print("\n" + "=" * 70)
        print("SOLUTION AGENT RETURNED INVALID JSON")
        print("=" * 70)

        print("\nRAW RESPONSE:")
        print(content)

        print("\nCLEANED RESPONSE:")
        print(cleaned)

        print("\nJSON ERROR:")
        print(str(e))

        print("=" * 70)

        raise ValueError(
            "Solution Agent returned invalid JSON."
        ) from e

    if not isinstance(
        result,
        dict
    ):

        raise ValueError(
            "Solution Agent response must be a JSON object."
        )

    return result


# =========================================================
# VALIDATE SOLUTION
# =========================================================

def validate_solution(result):
    """
    Validate the structure of the generated solution.
    """

    required_fields = [
        "problem",
        "root_cause",
        "root_cause_status",
        "evidence",
        "contradicting_evidence",
        "confidence",
        "solution",
        "corrected_code",
        "verification_steps",
        "prevention"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:

        raise ValueError(
            "Solution response is missing fields: "
            + ", ".join(missing_fields)
        )

    # -----------------------------------------------------
    # Convert required text fields to strings
    # -----------------------------------------------------

    text_fields = [
        "problem",
        "root_cause",
        "solution",
        "corrected_code",
        "prevention"
    ]

    for field in text_fields:

        if result[field] is None:

            result[field] = ""

        elif not isinstance(
            result[field],
            str
        ):

            result[field] = str(
                result[field]
            )

    # -----------------------------------------------------
    # Ensure verification_steps is a list
    # -----------------------------------------------------

    if not isinstance(
        result["verification_steps"],
        list
    ):

        result["verification_steps"] = [
            str(
                result["verification_steps"]
            )
        ]

    # -----------------------------------------------------
    # Normalize verification steps
    # -----------------------------------------------------

    result["verification_steps"] = [
        str(step)
        for step in result["verification_steps"]
    ]

    # -----------------------------------------------------
    # Validate root cause status
    # -----------------------------------------------------

    valid_statuses = {
        "CONFIRMED",
        "PROBABLE",
        "UNKNOWN"
    }

    status = str(
        result["root_cause_status"]
    ).upper().strip()

    if status not in valid_statuses:
        status = "UNKNOWN"

    result["root_cause_status"] = status

    # -----------------------------------------------------
    # Validate evidence fields
    # -----------------------------------------------------

    for field in [
        "evidence",
        "contradicting_evidence"
    ]:
        if result[field] is None:
            result[field] = []

        if not isinstance(result[field], list):
            result[field] = [str(result[field])]

        result[field] = [
            str(item)
            for item in result[field]
        ]

    # -----------------------------------------------------
    # Validate confidence
    # -----------------------------------------------------

    try:
        confidence = float(result["confidence"])
    except (TypeError, ValueError):
        confidence = 0

    confidence = max(
        0,
        min(100, confidence)
    )

    result["confidence"] = confidence

    return result


# =========================================================
# SOLUTION GENERATOR
# =========================================================

def generate_solution(
    error_message,
    classification,
    analysis,
    knowledge=None,
    code=None,
    tool_result=None,
    previous_verification=None
):
    """
    Generate an evidence-based debugging solution.

    Priority:

    1. Debugging tool evidence
    2. Specialist analysis
    3. Previous verification feedback
    4. RAG knowledge
    5. General debugging knowledge
    """

    # =====================================================
    # GET LLM
    # =====================================================

    llm = get_llm()

    # =====================================================
    # CONVERT INPUTS TO TEXT
    # =====================================================

    classification_text = json.dumps(
        classification or {},
        indent=2,
        default=str
    )

    analysis_text = json.dumps(
        analysis or {},
        indent=2,
        default=str
    )

    # -----------------------------------------------------
    # RAG knowledge
    # -----------------------------------------------------

    knowledge_text = (
        str(knowledge).strip()
        if knowledge
        else "No additional knowledge retrieved."
    )

    # -----------------------------------------------------
    # User code
    # -----------------------------------------------------

    code_text = (
        str(code).strip()
        if code
        else "No code was provided."
    )

    # -----------------------------------------------------
    # Debugging tool result
    # -----------------------------------------------------

    if tool_result:

        tool_result_text = json.dumps(
            tool_result,
            indent=2,
            default=str
        )

    else:

        tool_result_text = (
            "No debugging tool was executed."
        )

    # -----------------------------------------------------
    # Previous verification
    # -----------------------------------------------------

    if previous_verification:

        verification_text = json.dumps(
            previous_verification,
            indent=2,
            default=str
        )

        retry_context = f"""
A previous solution was rejected by the Verification Agent.

PREVIOUS VERIFICATION RESULT:
{verification_text}

The new solution MUST address the verifier's issues.

Do NOT blindly repeat the previous solution.

If the previous solution contradicts debugging evidence,
replace it with an evidence-based solution.
"""

    else:

        verification_text = (
            "No previous verification result is available."
        )

        retry_context = """
This is the first solution-generation attempt.

There is no previous verification feedback.
"""

    # =====================================================
    # SOLUTION PROMPT
    # =====================================================

    prompt = f"""
You are the Solution Agent in a multi-agent AI
software debugging system.

Your responsibility is to generate a technically
correct, evidence-based debugging solution.

You are NOT a generic chatbot.

You receive evidence from:

- Error Classifier
- Code Analysis
- RAG Knowledge Base
- Specialist Agent
- Debugging Tools
- Verification Agent

Your solution MUST be grounded in this evidence.

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
RAG KNOWLEDGE
==========================================================

{knowledge_text}


==========================================================
USER CODE
==========================================================

{code_text}


==========================================================
DEBUGGING TOOL RESULT
==========================================================

{tool_result_text}


==========================================================
PREVIOUS VERIFICATION
==========================================================

{verification_text}


==========================================================
RETRY CONTEXT
==========================================================

{retry_context}


==========================================================
EVIDENCE PRIORITY
==========================================================

Use evidence in this exact priority order:

1. DEBUGGING TOOL RESULT
2. SPECIALIST / CODE ANALYSIS
3. PREVIOUS VERIFICATION FEEDBACK
4. RAG KNOWLEDGE
5. GENERAL DEBUGGING KNOWLEDGE

The debugging tool contains actual runtime,
database, environment, configuration, or system
evidence.

Therefore:

NEVER contradict verified debugging tool evidence.


==========================================================
ROOT CAUSE PRIORITY RULE
==========================================================

When determining the root cause, distinguish the immediate
primary failure from broader environmental or contextual issues.

Use this priority order:

1. Direct exception or error message from the debugging tool.
2. Concrete tool state showing the failed component.
3. Code or specialist analysis identifying the failing operation.
4. Environment warnings, compatibility warnings, or general
   platform information.

The PRIMARY root cause must explain the immediate failure
reported by the tool.

Do NOT mark a broad environmental warning as the CONFIRMED
primary root cause when the debugging tool provides a more
specific direct exception.

When multiple issues are present:
- Identify the immediate failure as the PRIMARY root cause.
- Treat broader environment/configuration issues as secondary
  context unless they directly explain the exception.
- Include secondary issues in evidence when relevant.
- Use PROBABLE when the evidence strongly suggests the cause
  but does not uniquely prove it.
- Use UNKNOWN when the available evidence is insufficient.

A root cause may be CONFIRMED only when concrete evidence
directly establishes that it caused the reported failure.


==========================================================
CRITICAL DEBUGGING RULES
==========================================================

RULE 1
------

Identify the actual problem before proposing a fix.


RULE 2
------

Determine the root cause using available evidence.

Do not guess when evidence is available.


RULE 3
------

Use the debugging tool result as the strongest
source of truth.


RULE 4
------

NEVER propose a solution that contradicts the
debugging tool result.


RULE 5
------

If the tool says a package is installed, do NOT
recommend installing the package again unless there
is additional evidence showing that a different
environment is missing it.


RULE 6
------

If the tool says a package imports successfully,
do NOT assume the package is missing.

Investigate possible environment/interpreter mismatch.


RULE 7
------

If the tool says a database table exists,
do NOT recommend creating the table.


RULE 8
------

If the tool says a column does not exist,
do NOT invent a replacement column name.

Instead recommend inspecting the schema.


RULE 9
------

If a JOIN may be required, do not assume which table
or column should be joined.

Tell the user how to verify the relationship.


RULE 10
------

If a Docker daemon is not running, do not claim that
Docker containers are running successfully.


RULE 11
------

If a service is already running, do not recommend
starting it again without evidence that it is
unhealthy.


RULE 12
------

If a connection succeeds, do not claim that the
connection is the root cause.


RULE 13
------

Corrected code or commands MUST directly address
the identified root cause.


RULE 14
------

Do not provide a cosmetic code change as the fix when
the actual problem is environmental, configuration,
database, dependency, or infrastructure related.


RULE 15
------

If the evidence is contradictory, explicitly explain
the contradiction and provide diagnostic steps to
resolve it.


RULE 16
------

If this is a retry attempt, every issue identified
by the Verification Agent MUST be addressed.


RULE 17
------

Do not simply repeat a previously rejected solution.


RULE 18
------

If evidence is insufficient, clearly state what must
be checked instead of inventing an answer.


==========================================================
MANDATORY CONTRADICTION CHECK
==========================================================

Before producing the final solution, internally check:

1. What does the debugging tool prove?

2. What does the proposed root cause claim?

3. Do they agree?

4. What does the proposed solution assume?

5. Does the solution contradict any verified evidence?

6. Does the corrected code actually address the
   identified root cause?

If there is a contradiction:

DO NOT produce the contradictory solution.

Instead:

- explain the contradiction
- identify the likely reason
- provide diagnostic commands
- provide a safe next step


==========================================================
PRIMARY VS SECONDARY ROOT CAUSE EXAMPLE
==========================================================

Suppose a tool reports both:

- A specific exception such as:
  AirflowConfigException: Cannot use relative path:
  sqlite:///C:\\Users\\user\\airflow\\airflow.db

- A broader warning that native Windows execution is not
  supported or has compatibility limitations.

The SQLite connection/path exception is the PRIMARY immediate
failure because it is the concrete exception that terminated
the operation.

The Windows compatibility warning is SECONDARY CONTEXT unless
the available evidence directly proves that Windows caused the
specific exception.

Therefore, do NOT automatically produce:

root_cause_status: "CONFIRMED"
root_cause: "Airflow cannot run on Windows."

Instead, prefer:

root_cause_status: "PROBABLE"

root_cause:
"The immediate failure is caused by the invalid SQLite
connection/path configuration. Native Windows compatibility
is an additional environment constraint."

evidence:
- "Airflow raised AirflowConfigException for the SQLite URL."
- "The failing SQLite URL contains the Windows filesystem path."
- "Airflow also reported a Windows compatibility warning."

contradicting_evidence:
- "The evidence does not prove that Windows itself is the
  sole immediate cause of the SQLite configuration exception."

The exact wording may differ, but the primary exception must
remain the focus of the diagnosis.


==========================================================
IMPORTANT EXAMPLE
==========================================================

Suppose the original error is:

ModuleNotFoundError: No module named 'pandas'

But the debugging tool reports:

pandas installed = True
import successful = True
pandas version = 3.0.5

Then this is WRONG:

solution:
"Install pandas using pip."

This is also WRONG:

corrected_code:
"pip install pandas"

Because the tool already proved that pandas exists
and imports successfully.

Instead, the agent should reason:

The current debugging environment can import pandas,
so the failing process may be using a different
Python interpreter or virtual environment.

Useful verification commands include:

python -c "import sys; print(sys.executable)"

python -m pip --version

python -m pip show pandas

python -c "import pandas; print(pandas.__file__)"

The exact solution should be based on the resulting
evidence.


==========================================================
DATABASE EXAMPLE
==========================================================

Suppose the tool reports:

table_exists = true
column_exists = false

Do NOT say:

"Create the orders table."

Do NOT invent:

"Use customer_full_name instead."

Instead:

- confirm the actual schema
- inspect available columns
- check aliases
- determine whether a JOIN is required
- then modify the query


==========================================================
SAFE DEBUGGING
==========================================================

Prefer diagnostic and non-destructive commands.

Do not recommend:

- deleting databases
- dropping tables
- deleting production data
- exposing credentials
- destructive migrations

unless the user explicitly requests such an operation
and the evidence supports it.


==========================================================
OUTPUT REQUIREMENTS
==========================================================

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT use ```json.

Do NOT add explanations outside the JSON.

The JSON must contain EXACTLY these fields:

{{
    "problem": "string",

    "root_cause": "string",

    "root_cause_status": "CONFIRMED | PROBABLE | UNKNOWN",

    "evidence": [
        "string"
    ],

    "contradicting_evidence": [
        "string"
    ],

    "confidence": 0,

    "solution": "string",

    "corrected_code": "string",

    "verification_steps": [
        "string",
        "string"
    ],

    "prevention": "string"
}}


==========================================================
FIELD REQUIREMENTS
==========================================================

problem:
Describe what is actually failing.

root_cause:
Explain why the failure occurs using available evidence.

root_cause_status:
Use:
- CONFIRMED only when the direct debugging evidence establishes
  that the proposed root cause caused the immediate failure.
- PROBABLE when the evidence strongly suggests the root cause
  but does not uniquely prove it.
- UNKNOWN when the available evidence is insufficient.

Do not use CONFIRMED merely because an environmental warning,
compatibility warning, or general platform limitation is present.

evidence:
List the concrete facts from debugging tools, code analysis,
specialist analysis, or other available evidence that support
the root cause.

contradicting_evidence:
List any evidence that conflicts with the proposed root cause.
Use an empty list when there is no contradiction.

confidence:
Provide a number from 0 to 100 representing confidence
in the root cause.

IMPORTANT:
Do not use a high confidence value when evidence is contradictory
or insufficient.

solution:
Explain the recommended fix.

corrected_code:
Provide the corrected code or diagnostic commands.
If no code change is appropriate, provide the relevant
verification commands instead.

verification_steps:
Provide concrete steps that prove the fix works.

prevention:
Explain how to prevent the same issue in the future.
"""

    # =====================================================
    # CALL LLM
    # =====================================================

    try:

        response = llm.invoke(
            prompt
        )

    except Exception as e:

        error_text = str(e)

        # -------------------------------------------------
        # Detect rate limit
        # -------------------------------------------------

        if (
            "429" in error_text
            or "rate limit" in error_text.lower()
            or "resource_exhausted" in error_text.lower()
        ):

            raise RuntimeError(
                "LLM rate limit exceeded. "
                "Please wait for the quota to reset "
                "or configure a fallback LLM."
            ) from e

        # -------------------------------------------------
        # Other LLM errors
        # -------------------------------------------------

        raise RuntimeError(
            f"LLM invocation failed: {e}"
        ) from e

    # =====================================================
    # NORMALIZE RESPONSE
    # =====================================================

    content = normalize_response(
        response
    )

    # =====================================================
    # PARSE JSON
    # =====================================================

    result = parse_json_response(
        content
    )

    # =====================================================
    # VALIDATE RESULT
    # =====================================================

    result = validate_solution(
        result
    )

    # =====================================================
    # PRINT SOLUTION SUMMARY
    # =====================================================

    print("\n" + "=" * 70)
    print("SOLUTION AGENT")
    print("=" * 70)

    print("\nProblem:")
    print(
        result["problem"]
    )

    print("\nRoot Cause:")
    print(
        result["root_cause"]
    )

    print("\nRoot Cause Status:")
    print(
        result["root_cause_status"]
    )

    print("\nEvidence:")
    for item in result["evidence"]:
        print(f"- {item}")

    print("\nContradicting Evidence:")
    for item in result["contradicting_evidence"]:
        print(f"- {item}")

    print("\nConfidence:")
    print(
        f"{result['confidence']}%"
    )

    print("\nSolution:")
    print(
        result["solution"]
    )

    print("\nCorrected Code / Command:")
    print(
        result["corrected_code"]
    )

    print("\nVerification Steps:")

    for step in result[
        "verification_steps"
    ]:

        print(
            f"- {step}"
        )

    print("\nPrevention:")
    print(
        result["prevention"]
    )

    print("=" * 70)

    # =====================================================
    # RETURN
    # =====================================================

    return result
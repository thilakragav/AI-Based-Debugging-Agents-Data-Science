from pathlib import Path
import os
import json
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# =========================================================
# ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    ENV_FILE,
    override=True
)


# =========================================================
# GROQ MODEL
# =========================================================

def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in the .env file."
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=api_key
    )


# =========================================================
# NORMALIZE LLM RESPONSE
# =========================================================

def normalize_response(response):

    content = response.content

    # -----------------------------------------------------
    # LangChain may return a list of blocks
    # -----------------------------------------------------

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
# EXTRACT JSON
# =========================================================

def parse_json_response(content):

    content = content.strip()

    # -----------------------------------------------------
    # Remove Markdown fences
    # -----------------------------------------------------

    content = re.sub(
        r"^```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"^```\s*",
        "",
        content
    )

    content = re.sub(
        r"\s*```$",
        "",
        content
    )

    content = content.strip()

    # -----------------------------------------------------
    # Direct JSON parsing
    # -----------------------------------------------------

    try:

        return json.loads(content)

    except json.JSONDecodeError:
        pass

    # -----------------------------------------------------
    # Extract JSON object if LLM added extra text
    # -----------------------------------------------------

    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1:

        json_text = content[
            start:end + 1
        ]

        try:

            return json.loads(
                json_text
            )

        except json.JSONDecodeError:
            pass

    # -----------------------------------------------------
    # Invalid JSON
    # -----------------------------------------------------

    print("=" * 70)
    print("GROQ RETURNED INVALID JSON")
    print("=" * 70)
    print(content)
    print("=" * 70)

    raise ValueError(
        "Groq returned invalid JSON."
    )


# =========================================================
# CODE ANALYZER
# =========================================================

def analyze_code(
    error_message,
    code=None,
    classification=None
):

    # -----------------------------------------------------
    # Get Groq LLM
    # -----------------------------------------------------

    llm = get_llm()

    # -----------------------------------------------------
    # Classification
    # -----------------------------------------------------

    classification_text = json.dumps(
        classification or {},
        indent=2,
        default=str
    )

    # -----------------------------------------------------
    # Code
    # -----------------------------------------------------

    if not code:

        code = (
            "No code was provided by the user."
        )

    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt = f"""
You are an expert software debugging analyst.

Analyze the user's error, classification,
and source code.

Do not invent information.

Use only evidence available in:
- Error message
- Classification
- Source code

ERROR:
{error_message}

CLASSIFICATION:
{classification_text}

SOURCE CODE:
{code}

Determine:

1. What is wrong?
2. What is the likely root cause?
3. Which part of the code or environment is responsible?
4. What evidence supports the diagnosis?
5. What should be checked before applying a fix?
6. What is the severity?

IMPORTANT:

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT use ```json.

Do NOT add explanations outside JSON.

Use exactly this structure:

{{
    "problem": "...",
    "root_cause": "...",
    "responsible_component": "...",
    "evidence": "...",
    "recommended_checks": [
        "...",
        "..."
    ],
    "severity": "Low"
}}
"""

    # -----------------------------------------------------
    # Call Groq
    # -----------------------------------------------------

    response = llm.invoke(
        prompt
    )

    # -----------------------------------------------------
    # Normalize response
    # -----------------------------------------------------

    content = normalize_response(
        response
    )

    # -----------------------------------------------------
    # Parse JSON
    # -----------------------------------------------------

    result = parse_json_response(
        content
    )

    # -----------------------------------------------------
    # Validate required fields
    # -----------------------------------------------------

    required_fields = [
        "problem",
        "root_cause",
        "responsible_component",
        "evidence",
        "recommended_checks",
        "severity"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:

        raise ValueError(
            "Code analysis response is missing fields: "
            + ", ".join(missing_fields)
        )

    # -----------------------------------------------------
    # Return analysis
    # -----------------------------------------------------

    return result
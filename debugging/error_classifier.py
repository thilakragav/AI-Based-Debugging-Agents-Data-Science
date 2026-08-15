import json
import re

from debugging.llm import get_llm


# =========================================================
# DETERMINISTIC ERROR PATTERNS
# =========================================================

def detect_known_error(error_message):
    """
    Detect high-confidence errors using deterministic rules.

    Deterministic rules run before the LLM so well-known
    errors are classified consistently.
    """

    error = str(error_message or "").strip()
    text = error.lower()

    # =====================================================
    # AIRFLOW - HIGH PRIORITY
    # =====================================================
    # IMPORTANT:
    # This MUST appear before generic Python errors such as
    # NameError, ModuleNotFoundError, etc.
    #
    # Example:
    # Airflow DAG parsing failed:
    # NameError: name 'PythonOperator' is not defined
    #
    # Without this priority rule, the NameError rule below
    # would incorrectly classify the problem as Python.
    # =====================================================

    if (
        "airflow" in text
        or "airflow dag" in text
        or "dag parsing" in text
        or "pythonoperator" in text
        or "airflow.operators" in text
        or "airflow scheduler" in text
        or "airflow task" in text
    ):
        return {
            "technology": "Airflow",
            "error_type": "AirflowError",
            "category": "Workflow Error",
            "confidence": "High",
            "reason": (
                "The error contains explicit Airflow-specific "
                "DAG, operator, scheduler, task, or workflow information."
            )
        }

    # =====================================================
    # POSTGRESQL - UNDEFINED COLUMN
    # =====================================================

    if (
        (
            "column" in text
            and "does not exist" in text
        )
        or "undefinedcolumn" in text
    ):
        return {
            "technology": "PostgreSQL",
            "error_type": "UndefinedColumn",
            "category": "Database Error",
            "confidence": "High",
            "reason": (
                "The PostgreSQL error indicates that a referenced "
                "column does not exist in the target table or relation."
            )
        }

    # =====================================================
    # POSTGRESQL - UNDEFINED TABLE / RELATION
    # =====================================================

    if (
        (
            "relation" in text
            and "does not exist" in text
        )
        or "undefinedtable" in text
    ):
        return {
            "technology": "PostgreSQL",
            "error_type": "UndefinedTable",
            "category": "Database Error",
            "confidence": "High",
            "reason": (
                "PostgreSQL cannot resolve the referenced table "
                "or relation."
            )
        }

    # =====================================================
    # POSTGRESQL - DUPLICATE COLUMN
    # =====================================================

    if (
        "duplicate column" in text
        or "column already exists" in text
    ):
        return {
            "technology": "PostgreSQL",
            "error_type": "DuplicateColumn",
            "category": "Database Error",
            "confidence": "High",
            "reason": (
                "The PostgreSQL operation references or attempts "
                "to create a duplicate column."
            )
        }

    # =====================================================
    # POSTGRESQL - UNIQUE VIOLATION
    # =====================================================

    if (
        "unique constraint" in text
        or "duplicate key value violates unique constraint" in text
    ):
        return {
            "technology": "PostgreSQL",
            "error_type": "UniqueViolation",
            "category": "Database Error",
            "confidence": "High",
            "reason": (
                "The operation violates a PostgreSQL unique "
                "constraint."
            )
        }

    # =====================================================
    # POSTGRESQL - FOREIGN KEY
    # =====================================================

    if (
        "foreign key constraint" in text
        or "violates foreign key constraint" in text
    ):
        return {
            "technology": "PostgreSQL",
            "error_type": "ForeignKeyViolation",
            "category": "Database Error",
            "confidence": "High",
            "reason": (
                "The operation violates a PostgreSQL foreign "
                "key constraint."
            )
        }

    # =====================================================
    # DOCKER - DAEMON ERROR
    # =====================================================

    if (
        "docker daemon" in text
        or "docker is not running" in text
        or "cannot connect to the docker daemon" in text
        or "failed to connect to the docker api" in text
        or "dockerdesktoplinuxengine" in text
    ):
        return {
            "technology": "Docker",
            "error_type": "DockerDaemonError",
            "category": "Docker Error",
            "confidence": "High",
            "reason": (
                "The Docker client cannot connect to the "
                "Docker daemon."
            )
        }

    # =====================================================
    # DOCKER - IMAGE / REPOSITORY ERROR
    # =====================================================

    if (
        "unable to find image" in text
        or "pull access denied" in text
        or "repository does not exist" in text
        or "docker image" in text
    ):
        return {
            "technology": "Docker",
            "error_type": "ImagePullError",
            "category": "Docker Error",
            "confidence": "High",
            "reason": (
                "Docker could not locate or pull the requested "
                "container image or repository."
            )
        }

    # =====================================================
    # PYTHON - MODULE NOT FOUND
    # =====================================================

    if "modulenotfounderror" in text:
        return {
            "technology": "Python",
            "error_type": "ModuleNotFoundError",
            "category": "Import Error",
            "confidence": "High",
            "reason": (
                "Python cannot find the requested module."
            )
        }

    # =====================================================
    # PYTHON - NAME ERROR
    # =====================================================

    if "nameerror" in text:
        return {
            "technology": "Python",
            "error_type": "NameError",
            "category": "Runtime Error",
            "confidence": "High",
            "reason": (
                "Python is referencing a name that has not "
                "been defined or is not available in scope."
            )
        }

    # =====================================================
    # PYTHON - KEY ERROR
    # =====================================================

    if "keyerror" in text:
        return {
            "technology": "Python",
            "error_type": "KeyError",
            "category": "Runtime Error",
            "confidence": "High",
            "reason": (
                "Python attempted to access a dictionary key "
                "that does not exist."
            )
        }

    # =====================================================
    # PYTHON - TYPE ERROR
    # =====================================================

    if "typeerror" in text:
        return {
            "technology": "Python",
            "error_type": "TypeError",
            "category": "Runtime Error",
            "confidence": "High",
            "reason": (
                "Python encountered an operation involving "
                "an incompatible type."
            )
        }

    # =====================================================
    # PYTHON - INDEX ERROR
    # =====================================================

    if "indexerror" in text:
        return {
            "technology": "Python",
            "error_type": "IndexError",
            "category": "Runtime Error",
            "confidence": "High",
            "reason": (
                "Python attempted to access an invalid list "
                "or sequence index."
            )
        }

    # =====================================================
    # SQL - SYNTAX ERROR
    # =====================================================

    if (
        "sql syntax" in text
        or "syntax error at or near" in text
        or "syntax error" in text
    ):
        return {
            "technology": "SQL",
            "error_type": "SyntaxError",
            "category": "Database Query Error",
            "confidence": "High",
            "reason": (
                "The error indicates that the SQL statement "
                "contains invalid or malformed syntax."
            )
        }

    # =====================================================
    # SQL - INVALID QUERY
    # =====================================================

    if (
        "invalid sql" in text
        or "invalid query" in text
        or "query failed" in text
    ):
        return {
            "technology": "SQL",
            "error_type": "QueryError",
            "category": "Database Query Error",
            "confidence": "High",
            "reason": (
                "The database rejected the SQL query."
            )
        }

    # =====================================================
    # NO DETERMINISTIC MATCH
    # =====================================================

    return None


# =========================================================
# ERROR CLASSIFIER
# =========================================================

def classify_error(error_message):

    # -----------------------------------------------------
    # FIRST: DETERMINISTIC CLASSIFICATION
    # -----------------------------------------------------

    known_error = detect_known_error(
        error_message
    )

    if known_error:

        print("=" * 60)
        print("DETERMINISTIC ERROR CLASSIFICATION")
        print("=" * 60)

        print(
            "Technology    :",
            known_error["technology"]
        )

        print(
            "Category      :",
            known_error["category"]
        )

        print(
            "Error Type    :",
            known_error["error_type"]
        )

        print(
            "Confidence    :",
            known_error["confidence"]
        )

        print("=" * 60)

        return known_error

    # -----------------------------------------------------
    # FALLBACK TO LLM
    # -----------------------------------------------------

    llm = get_llm()

    prompt = f"""
You are an AI software debugging classifier.

Analyze the following error message:

ERROR:
{error_message}

Classify the error into exactly ONE of these technologies:

- Python
- SQL
- Airflow
- Docker
- PostgreSQL
- Unknown

IMPORTANT CLASSIFICATION RULES:

1. If the error explicitly mentions Airflow, DAG,
   scheduler, Airflow task, PythonOperator, or
   airflow.operators, classify it as Airflow.

2. If an error contains both Airflow context and
   a generic Python error such as NameError or
   ModuleNotFoundError, prioritize Airflow.

3. Only classify a generic NameError, KeyError,
   TypeError, IndexError, or ModuleNotFoundError
   as Python when there is no explicit Airflow context.

Return ONLY valid JSON.

Do not use Markdown.
Do not use ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "technology": "...",
    "error_type": "...",
    "category": "...",
    "confidence": "High/Medium/Low",
    "reason": "..."
}}

Error to classify:
{error_message}
"""

    # -----------------------------------------------------
    # CALL LLM
    # -----------------------------------------------------

    response = llm.invoke(prompt)

    content = response.content

    # -----------------------------------------------------
    # HANDLE LIST CONTENT
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

    # -----------------------------------------------------
    # CONVERT TO STRING
    # -----------------------------------------------------

    content = str(content).strip()

    # -----------------------------------------------------
    # REMOVE MARKDOWN
    # -----------------------------------------------------

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    # -----------------------------------------------------
    # EXTRACT JSON
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

    # -----------------------------------------------------
    # PARSE JSON
    # -----------------------------------------------------

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        print("=" * 60)
        print("LLM RETURNED INVALID JSON")
        print("=" * 60)

        print(content)

        raise ValueError(
            "LLM returned an invalid JSON response."
        )

    # -----------------------------------------------------
    # VALIDATE REQUIRED FIELDS
    # -----------------------------------------------------

    required_fields = [
        "technology",
        "error_type",
        "category",
        "confidence",
        "reason"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:

        raise ValueError(
            "Classification response is missing fields: "
            + ", ".join(missing_fields)
        )

    # -----------------------------------------------------
    # NORMALIZE TECHNOLOGY
    # -----------------------------------------------------

    technology = str(
        result["technology"]
    ).strip()

    allowed_technologies = {
        "Python",
        "SQL",
        "Airflow",
        "Docker",
        "PostgreSQL",
        "Unknown"
    }

    if technology not in allowed_technologies:

        result["technology"] = "Unknown"

    # -----------------------------------------------------
    # RETURN CLASSIFICATION
    # -----------------------------------------------------

    return result
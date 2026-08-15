import os
import re

import psycopg2
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv(
    override=True
)


# =========================================================
# POSTGRESQL CONNECTION
# =========================================================

def check_postgresql_connection():

    host = os.getenv(
        "POSTGRES_HOST",
        "localhost"
    )

    port = os.getenv(
        "POSTGRES_PORT",
        "5432"
    )

    database = os.getenv(
        "POSTGRES_DB"
    )

    user = os.getenv(
        "POSTGRES_USER"
    )

    password = os.getenv(
        "POSTGRES_PASSWORD"
    )

    # -----------------------------------------------------
    # Check configuration
    # -----------------------------------------------------

    if not database or not user or not password:

        return {
            "connected": False,
            "error": (
                "PostgreSQL connection details "
                "are not configured."
            )
        }

    # -----------------------------------------------------
    # Connect
    # -----------------------------------------------------

    try:

        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connect_timeout=5
        )

        connection.close()

        return {
            "connected": True,
            "host": host,
            "port": port,
            "database": database,
            "user": user
        }

    except Exception as e:

        return {
            "connected": False,
            "error": str(e)
        }


# =========================================================
# CHECK TABLE
# =========================================================

def check_postgresql_table(
    table_name,
    schema="public"
):

    connection_info = (
        check_postgresql_connection()
    )

    if not connection_info.get(
        "connected"
    ):

        return connection_info

    connection = None
    cursor = None

    try:

        connection = psycopg2.connect(
            host=os.getenv(
                "POSTGRES_HOST",
                "localhost"
            ),
            port=os.getenv(
                "POSTGRES_PORT",
                "5432"
            ),
            database=os.getenv(
                "POSTGRES_DB"
            ),
            user=os.getenv(
                "POSTGRES_USER"
            ),
            password=os.getenv(
                "POSTGRES_PASSWORD"
            )
        )

        cursor = connection.cursor()

        query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s
        );
        """

        cursor.execute(
            query,
            (
                schema,
                table_name
            )
        )

        exists = cursor.fetchone()[0]

        return {
            "table": table_name,
            "schema": schema,
            "exists": exists
        }

    except Exception as e:

        return {
            "table": table_name,
            "schema": schema,
            "exists": False,
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# CHECK COLUMN
# =========================================================

def check_postgresql_column(
    table_name,
    column_name,
    schema="public"
):

    connection_info = (
        check_postgresql_connection()
    )

    if not connection_info.get(
        "connected"
    ):

        return connection_info

    connection = None
    cursor = None

    try:

        connection = psycopg2.connect(
            host=os.getenv(
                "POSTGRES_HOST",
                "localhost"
            ),
            port=os.getenv(
                "POSTGRES_PORT",
                "5432"
            ),
            database=os.getenv(
                "POSTGRES_DB"
            ),
            user=os.getenv(
                "POSTGRES_USER"
            ),
            password=os.getenv(
                "POSTGRES_PASSWORD"
            )
        )

        cursor = connection.cursor()

        query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = %s
            AND table_name = %s
            AND column_name = %s
        );
        """

        cursor.execute(
            query,
            (
                schema,
                table_name,
                column_name
            )
        )

        exists = cursor.fetchone()[0]

        return {
            "table": table_name,
            "column": column_name,
            "schema": schema,
            "exists": exists
        }

    except Exception as e:

        return {
            "table": table_name,
            "column": column_name,
            "schema": schema,
            "exists": False,
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# GET TABLE COLUMNS
# =========================================================

def get_postgresql_table_columns(
    table_name,
    schema="public"
):

    connection = None
    cursor = None

    try:

        connection = psycopg2.connect(
            host=os.getenv(
                "POSTGRES_HOST",
                "localhost"
            ),
            port=os.getenv(
                "POSTGRES_PORT",
                "5432"
            ),
            database=os.getenv(
                "POSTGRES_DB"
            ),
            user=os.getenv(
                "POSTGRES_USER"
            ),
            password=os.getenv(
                "POSTGRES_PASSWORD"
            )
        )

        cursor = connection.cursor()

        query = """
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        ORDER BY ordinal_position;
        """

        cursor.execute(
            query,
            (
                schema,
                table_name
            )
        )

        rows = cursor.fetchall()

        return {
            "table": table_name,
            "schema": schema,
            "columns": [
                {
                    "name": row[0],
                    "data_type": row[1]
                }
                for row in rows
            ]
        }

    except Exception as e:

        return {
            "table": table_name,
            "schema": schema,
            "columns": [],
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# FIND COLUMN ACROSS DATABASE
# =========================================================

def find_postgresql_column(
    column_name,
    schema="public"
):

    connection = None
    cursor = None

    try:

        connection = psycopg2.connect(
            host=os.getenv(
                "POSTGRES_HOST",
                "localhost"
            ),
            port=os.getenv(
                "POSTGRES_PORT",
                "5432"
            ),
            database=os.getenv(
                "POSTGRES_DB"
            ),
            user=os.getenv(
                "POSTGRES_USER"
            ),
            password=os.getenv(
                "POSTGRES_PASSWORD"
            )
        )

        cursor = connection.cursor()

        query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        AND column_name = %s
        ORDER BY table_name;
        """

        cursor.execute(
            query,
            (
                schema,
                column_name
            )
        )

        rows = cursor.fetchall()

        return {
            "column": column_name,
            "matches": [
                {
                    "table": row[0],
                    "column": row[1],
                    "data_type": row[2]
                }
                for row in rows
            ]
        }

    except Exception as e:

        return {
            "column": column_name,
            "matches": [],
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# FIND RELATED TABLES
# =========================================================

def find_postgresql_related_tables(
    table_name,
    column_name,
    schema="public"
):

    connection = None
    cursor = None

    try:

        connection = psycopg2.connect(
            host=os.getenv(
                "POSTGRES_HOST",
                "localhost"
            ),
            port=os.getenv(
                "POSTGRES_PORT",
                "5432"
            ),
            database=os.getenv(
                "POSTGRES_DB"
            ),
            user=os.getenv(
                "POSTGRES_USER"
            ),
            password=os.getenv(
                "POSTGRES_PASSWORD"
            )
        )

        cursor = connection.cursor()

        query = """
        SELECT
            kcu.table_name AS source_table,
            kcu.column_name AS source_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = %s
        AND kcu.table_name = %s;
        """

        cursor.execute(
            query,
            (
                schema,
                table_name
            )
        )

        rows = cursor.fetchall()

        relationships = []

        for row in rows:

            relationships.append({
                "source_table": row[0],
                "source_column": row[1],
                "target_table": row[2],
                "target_column": row[3]
            })

        return {
            "table": table_name,
            "column": column_name,
            "relationships": relationships
        }

    except Exception as e:

        return {
            "table": table_name,
            "column": column_name,
            "relationships": [],
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# GENERATE JOIN SUGGESTION
# =========================================================

def generate_postgresql_join_suggestion(
    source_table,
    missing_column,
    source_code,
    schema="public"
):

    column_result = find_postgresql_column(
        missing_column,
        schema
    )

    matches = column_result.get(
        "matches",
        []
    )

    if not matches:

        return {
            "found": False,
            "reason": (
                f"Column '{missing_column}' "
                "was not found in other tables."
            )
        }

    suggestions = []

    source_columns_result = (
        get_postgresql_table_columns(
            source_table,
            schema
        )
    )

    source_columns = {
        column["name"]
        for column in source_columns_result.get(
            "columns",
            []
        )
    }

    for match in matches:

        target_table = match["table"]

        if target_table == source_table:
            continue

        target_columns_result = (
            get_postgresql_table_columns(
                target_table,
                schema
            )
        )

        target_columns = {
            column["name"]
            for column in target_columns_result.get(
                "columns",
                []
            )
        }

        common_columns = (
            source_columns.intersection(
                target_columns
            )
        )

        # Prefer ID/key columns for JOINs
        join_columns = [
            column
            for column in common_columns
            if column.lower().endswith("_id")
        ]

        if not join_columns:
            join_columns = list(
                common_columns
            )

        for join_column in join_columns:

            source_alias = "s"
            target_alias = "t"

            corrected_sql = (
                f"SELECT {target_alias}.{missing_column}, "
                f"{source_alias}.order_id\n"
                f"FROM {source_table} {source_alias}\n"
                f"JOIN {target_table} {target_alias}\n"
                f"    ON {source_alias}.{join_column} = "
                f"{target_alias}.{join_column};"
            )

            suggestions.append({
                "source_table": source_table,
                "target_table": target_table,
                "join_column": join_column,
                "missing_column": missing_column,
                "corrected_sql": corrected_sql
            })

    if not suggestions:

        return {
            "found": True,
            "column_locations": matches,
            "suggestions": [],
            "reason": (
                "The missing column was found, "
                "but no common JOIN column was detected."
            )
        }

    return {
        "found": True,
        "column_locations": matches,
        "suggestions": suggestions
    }



# =========================================================
# VALIDATE CORRECTED SQL
# =========================================================

def validate_postgresql_sql(
    sql,
    max_rows=10
):
    """
    Execute a read-only PostgreSQL query and verify
    whether the corrected SQL works.

    Only SELECT queries are allowed.
    """

    connection = None
    cursor = None

    if not sql:
        return {
            "success": False,
            "error": "No SQL query was provided."
        }

    # =====================================================
    # SAFETY CHECK
    # =====================================================

    normalized_sql = sql.strip().lower()

    if not normalized_sql.startswith("select"):
        return {
            "success": False,
            "error": (
                "SQL validation only allows SELECT queries."
            )
        }

    # Prevent multiple SQL statements.
    # A single trailing semicolon is allowed.
    sql_without_trailing_semicolon = normalized_sql.rstrip()

    if sql_without_trailing_semicolon.endswith(";"):
        sql_without_trailing_semicolon = (
            sql_without_trailing_semicolon[:-1].rstrip()
        )

    if ";" in sql_without_trailing_semicolon:
        return {
            "success": False,
            "error": (
                "Multiple SQL statements are not allowed."
            )
        }

    try:

        # =================================================
        # CONNECT
        # =================================================

        connection = psycopg2.connect(
            host=os.getenv(
                "POSTGRES_HOST",
                "localhost"
            ),
            port=os.getenv(
                "POSTGRES_PORT",
                "5432"
            ),
            database=os.getenv(
                "POSTGRES_DB"
            ),
            user=os.getenv(
                "POSTGRES_USER"
            ),
            password=os.getenv(
                "POSTGRES_PASSWORD"
            ),
            connect_timeout=5
        )

        # =================================================
        # READ-ONLY TRANSACTION
        # =================================================

        connection.set_session(
            readonly=True
        )

        cursor = connection.cursor()

        # =================================================
        # EXECUTE QUERY
        # =================================================

        cursor.execute(sql)

        rows = cursor.fetchmany(max_rows)

        column_names = []

        if cursor.description:
            column_names = [
                description[0]
                for description in cursor.description
            ]

        return {
            "success": True,
            "sql": sql,
            "columns": column_names,
            "rows_returned": len(rows),
            "sample_rows": [
                list(row)
                for row in rows
            ],
            "message": (
                "Corrected SQL executed successfully."
            )
        }

    except Exception as e:

        return {
            "success": False,
            "sql": sql,
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# POSTGRESQL DEBUGGING TOOL
# =========================================================

def execute_postgresql_debugging(
    error_message,
    classification,
    code=None
):

    result = {
        "technology": "postgresql",
        "tool_executed": True,
        "error_message": error_message,
        "error_type": "Unknown"
    }

    # =====================================================
    # CONNECTION CHECK
    # =====================================================

    result["connection"] = (
        check_postgresql_connection()
    )

    # =====================================================
    # NORMALIZE ERROR
    # =====================================================

    error_lower = (
        error_message.lower()
    )

    # =====================================================
    # DETECT ERROR TYPE
    # =====================================================

    if (
        "column" in error_lower
        and "does not exist" in error_lower
    ):

        result["error_type"] = (
            "ColumnNotFound"
        )

    elif (
        "relation" in error_lower
        and "does not exist" in error_lower
    ):

        result["error_type"] = (
            "TableNotFound"
        )

    elif "connection refused" in error_lower:

        result["error_type"] = (
            "ConnectionError"
        )

    elif (
        "password authentication failed"
        in error_lower
    ):

        result["error_type"] = (
            "AuthenticationError"
        )

    else:

        result["error_type"] = (
            classification.get(
                "error_type",
                "Unknown"
            )
        )

    # =====================================================
    # EXTRACT COLUMN NAME
    # =====================================================

    column_name = None

    column_match = re.search(
        r'column\s+"?([a-zA-Z_][a-zA-Z0-9_]*)"?'
        r'\s+does not exist',
        error_message,
        re.IGNORECASE
    )

    if column_match:

        column_name = (
            column_match.group(1)
        )

    result["column_name"] = (
        column_name
    )

    # =====================================================
    # EXTRACT TABLE NAME FROM SQL
    # =====================================================

    table_name = None

    if code:

        table_match = re.search(
            r'\bFROM\s+'
            r'([a-zA-Z_][a-zA-Z0-9_]*)',
            code,
            re.IGNORECASE
        )

        if table_match:

            table_name = (
                table_match.group(1)
            )

        # -------------------------------------------------
        # Try JOIN if FROM wasn't found
        # -------------------------------------------------

        if not table_name:

            join_match = re.search(
                r'\bJOIN\s+'
                r'([a-zA-Z_][a-zA-Z0-9_]*)',
                code,
                re.IGNORECASE
            )

            if join_match:

                table_name = (
                    join_match.group(1)
                )

    result["table_name"] = (
        table_name
    )

    # =====================================================
    # CHECK TABLE
    # =====================================================

    if table_name:

        result["table"] = (
            check_postgresql_table(
                table_name
            )
        )

    # =====================================================
    # CHECK COLUMN
    # =====================================================

    if (
        table_name
        and column_name
    ):

        result["column"] = (
            check_postgresql_column(
                table_name=table_name,
                column_name=column_name
            )
        )

    # =====================================================
    # SCHEMA INSPECTION
    # =====================================================

    if table_name:

        result["schema"] = (
            get_postgresql_table_columns(
                table_name
            )
        )

    # =====================================================
    # SEARCH FOR MISSING COLUMN
    # =====================================================

    if (
        column_name
        and table_name
        and result["error_type"]
        == "ColumnNotFound"
    ):

        result["column_search"] = (
            find_postgresql_column(
                column_name
            )
        )

        # =================================================
        # JOIN ANALYSIS
        # =================================================

        result["join_analysis"] = (
            generate_postgresql_join_suggestion(
                source_table=table_name,
                missing_column=column_name,
                source_code=code
            )
        )

    # =====================================================
    # BUILD EVIDENCE
    # =====================================================

    evidence = []

    # -----------------------------------------------------
    # Connection evidence
    # -----------------------------------------------------

    if result["connection"].get(
        "connected"
    ):

        evidence.append(
            "PostgreSQL connection succeeded."
        )

    else:

        evidence.append(
            "PostgreSQL connection failed."
        )

    # -----------------------------------------------------
    # Table evidence
    # -----------------------------------------------------

    if (
        table_name
        and "table" in result
    ):

        if result["table"].get(
            "exists"
        ):

            evidence.append(
                f"Table '{table_name}' exists."
            )

        else:

            evidence.append(
                f"Table '{table_name}' "
                f"does not exist."
            )

    # -----------------------------------------------------
    # Column evidence
    # -----------------------------------------------------

    if (
        column_name
        and "column" in result
    ):

        if result["column"].get(
            "exists"
        ):

            evidence.append(
                f"Column '{column_name}' "
                f"exists in table "
                f"'{table_name}'."
            )

        else:

            evidence.append(
                f"Column '{column_name}' "
                f"does not exist in table "
                f"'{table_name}'."
            )

    # -----------------------------------------------------
    # Schema evidence
    # -----------------------------------------------------

    if "schema" in result:

        columns = result["schema"].get(
            "columns",
            []
        )

        if columns:

            column_names = [
                column["name"]
                for column in columns
            ]

            evidence.append(
                f"Table '{table_name}' contains "
                f"columns: {', '.join(column_names)}."
            )

    # -----------------------------------------------------
    # Missing column location
    # -----------------------------------------------------

    if "column_search" in result:

        matches = result[
            "column_search"
        ].get(
            "matches",
            []
        )

        if matches:

            locations = [
                f"{match['table']}.{match['column']}"
                for match in matches
            ]

            evidence.append(
                f"Column '{column_name}' "
                f"was found in: "
                f"{', '.join(locations)}."
            )

    # -----------------------------------------------------
    # JOIN evidence
    # -----------------------------------------------------

    if "join_analysis" in result:

        suggestions = result[
            "join_analysis"
        ].get(
            "suggestions",
            []
        )

        if suggestions:

            first_suggestion = suggestions[0]

            evidence.append(
                f"A possible JOIN was detected between "
                f"'{first_suggestion['source_table']}' "
                f"and '{first_suggestion['target_table']}' "
                f"using '{first_suggestion['join_column']}'."
            )

            result["corrected_sql"] = (
                first_suggestion[
                    "corrected_sql"
                ]
            )

            # =================================================
            # VALIDATE CORRECTED SQL
            # =================================================

            result["sql_validation"] = (
                validate_postgresql_sql(
                    result["corrected_sql"]
                )
            )

    # -----------------------------------------------------
    # SQL validation evidence
    # -----------------------------------------------------

    if "sql_validation" in result:

        validation = result[
            "sql_validation"
        ]

        if validation.get("success"):

            evidence.append(
                "Corrected SQL executed successfully."
            )

            evidence.append(
                f"Validation returned "
                f"{validation.get('rows_returned', 0)} "
                f"sample rows."
            )

        else:

            evidence.append(
                "Corrected SQL validation failed: "
                + validation.get(
                    "error",
                    "Unknown SQL validation error."
                )
            )

    result["evidence"] = evidence

    return result
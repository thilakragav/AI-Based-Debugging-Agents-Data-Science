from langgraph.graph import StateGraph, START, END

from agent.state import DebuggingState

from agent.tools import (
    classification_tool,
    analysis_tool,
    debugging_tool_router,

    execute_python_debugging,
    execute_sql_debugging,
    execute_postgresql_tool,
    execute_docker_tool,
    execute_airflow_tool,
)


# =========================================================
# AGENTS
# =========================================================

from agent.agents.rag_agent import rag_agent
from agent.agents.supervisor_agent import supervisor_agent

from agent.agents.python_agent import python_agent
from agent.agents.sql_agent import sql_agent
from agent.agents.postgresql_agent import postgresql_agent
from agent.agents.docker_agent import docker_agent
from agent.agents.airflow_agent import airflow_agent
from agent.agents.solution_agent import solution_agent
from agent.agents.verification_agent import verification_agent


# =========================================================
# NODE 1 — CLASSIFY ERROR
# =========================================================

def classify_node(state: DebuggingState):
    """
    Classify the user's error.

    Also normalizes PostgreSQL-specific errors so that
    PostgreSQL problems are routed to the PostgreSQL
    specialist instead of the generic SQL specialist.
    """

    error_message = state.get(
        "error_message",
        ""
    )

    classification = classification_tool(
        error_message
    )

    if not isinstance(
        classification,
        dict
    ):
        classification = {}

    # -----------------------------------------------------
    # Normalize PostgreSQL-specific errors
    # -----------------------------------------------------

    error_text = str(
        error_message
    ).lower()

    postgres_markers = (
        "postgresql",
        "postgres",
        "psycopg",
        "psycopg2",
        "undefinedcolumn",
        "undefined column",
        "undefinedtable",
        "undefined table",
        "duplicate key value violates unique constraint",
        "foreign key violation",
        "relation does not exist",
        "does not exist",
        "pg_hba.conf",
        "password authentication failed for user",
        "connection refused",
    )

    current_technology = (
        str(
            classification.get(
                "technology",
                ""
            )
        )
        .lower()
        .strip()
    )

    if (
        current_technology == "sql"
        and any(
            marker in error_text
            for marker in postgres_markers
        )
    ):

        classification[
            "technology"
        ] = "postgresql"

    # -----------------------------------------------------
    # Display classification
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("CLASSIFICATION")
    print("=" * 60)

    print(
        f"Technology    : "
        f"{classification.get('technology', 'unknown')}"
    )

    print(
        f"Category      : "
        f"{classification.get('category', 'unknown')}"
    )

    print(
        f"Error Type    : "
        f"{classification.get('error_type', 'unknown')}"
    )

    print("=" * 60)

    return {
        "classification": classification
    }


# =========================================================
# NODE 2 — ANALYZE ERROR
# =========================================================

def analyze_node(
    state: DebuggingState
):
    """
    Analyze the error and user code.
    """

    error_message = state.get(
        "error_message",
        ""
    )

    classification = state.get(
        "classification",
        {}
    )

    code = state.get(
        "code",
        ""
    )

    analysis = analysis_tool(
        error_message=error_message,
        classification=classification,
        code=code
    )

    return {
        "analysis": analysis
    }


# =========================================================
# NODE 3 — RAG AGENT
# =========================================================

def rag_node(
    state: DebuggingState
):
    """
    Retrieve relevant debugging knowledge.
    """

    result = rag_agent(
        state
    )

    return {
        "rag_context": result.get(
            "rag_context",
            ""
        ),

        "retrieved_documents": result.get(
            "retrieved_documents",
            []
        )
    }


# =========================================================
# NODE 4 — SUPERVISOR AGENT
# =========================================================

def supervisor_node(
    state: DebuggingState
):
    """
    Supervisor selects the correct specialist agent.
    """

    result = supervisor_agent(
        state
    )

    selected_agent = result.get(
        "selected_agent",
        "sql_agent"
    )

    routing_reason = result.get(
        "routing_reason",
        ""
    )

    print("\n" + "=" * 60)
    print("SUPERVISOR ROUTING")
    print("=" * 60)

    print(
        f"Selected Agent : {selected_agent}"
    )

    print(
        f"Reason         : {routing_reason}"
    )

    print("=" * 60)

    return {
        "selected_agent": selected_agent,
        "routing_reason": routing_reason
    }


# =========================================================
# NODE 5A — PYTHON SPECIALIST
# =========================================================

def python_specialist_node(
    state: DebuggingState
):

    result = python_agent(
        state
    )

    return {
        "specialist_analysis":
            result.get(
                "specialist_analysis",
                {}
            )
    }


# =========================================================
# NODE 5B — SQL SPECIALIST
# =========================================================

def sql_specialist_node(
    state: DebuggingState
):

    result = sql_agent(
        state
    )

    return {
        "specialist_analysis":
            result.get(
                "specialist_analysis",
                {}
            )
    }


# =========================================================
# NODE 5C — POSTGRESQL SPECIALIST
# =========================================================

def postgresql_specialist_node(
    state: DebuggingState
):

    result = postgresql_agent(
        state
    )

    return {
        "specialist_analysis":
            result.get(
                "specialist_analysis",
                {}
            )
    }


# =========================================================
# NODE 5D — DOCKER SPECIALIST
# =========================================================

def docker_specialist_node(
    state: DebuggingState
):

    result = docker_agent(
        state
    )

    return {
        "specialist_analysis":
            result.get(
                "specialist_analysis",
                {}
            )
    }


# =========================================================
# NODE 5E — AIRFLOW SPECIALIST
# =========================================================

def airflow_specialist_node(
    state: DebuggingState
):

    result = airflow_agent(
        state
    )

    return {
        "specialist_analysis":
            result.get(
                "specialist_analysis",
                {}
            )
    }


# =========================================================
# SUPERVISOR ROUTER
# =========================================================

def specialist_router(
    state: DebuggingState
):
    """
    Route to the selected specialist agent.
    """

    selected_agent = state.get(
        "selected_agent",
        "sql_agent"
    )

    valid_agents = {
        "python_agent",
        "sql_agent",
        "postgresql_agent",
        "docker_agent",
        "airflow_agent"
    }

    if selected_agent not in valid_agents:

        print(
            f"Unknown agent '{selected_agent}'. "
            f"Defaulting to sql_agent."
        )

        return "sql_agent"

    return selected_agent


# =========================================================
# NODE 6 — DEBUGGING TOOL
# =========================================================

def debugging_tool_node(
    state: DebuggingState
):
    """
    Execute the technology-specific debugging tool.
    """

    error_message = state.get(
        "error_message",
        ""
    )

    classification = state.get(
        "classification",
        {}
    )

    code = state.get(
        "code",
        ""
    )

    route = debugging_tool_router(
        classification
    )

    selected_tool = route.get(
        "tool",
        "general_debugging"
    )

    print("\n" + "=" * 60)
    print("DEBUGGING TOOL")
    print("=" * 60)

    print(
        f"Tool: {selected_tool}"
    )

    # =====================================================
    # PYTHON
    # =====================================================

    if selected_tool == "execute_python_debugging":

        tool_result = execute_python_debugging(
            error_message=error_message,
            classification=classification
        )

    # =====================================================
    # SQL
    # =====================================================

    elif selected_tool == "execute_sql_debugging":

        tool_result = execute_sql_debugging(
            error_message=error_message,
            classification=classification,
            code=code
        )

    # =====================================================
    # POSTGRESQL
    # =====================================================

    elif selected_tool == "execute_postgresql_tool":

        tool_result = execute_postgresql_tool(
            error_message=error_message,
            classification=classification,
            code=code
        )

    # =====================================================
    # DOCKER
    # =====================================================

    elif selected_tool in (
        "execute_docker_debugging",
        "execute_docker_tool"
    ):

        tool_result = execute_docker_tool(
            error_message=error_message,
            classification=classification,
            code=code
        )

    # =====================================================
    # AIRFLOW
    # =====================================================

    elif selected_tool in (
        "execute_airflow_debugging",
        "execute_airflow_tool"
    ):

        tool_result = execute_airflow_tool(
            error_message=error_message,
            classification=classification,
            code=code
        )

    # =====================================================
    # UNKNOWN
    # =====================================================

    else:

        tool_result = {
            "technology": classification.get(
                "technology",
                "unknown"
            ),

            "tool_executed": False,

            "message": (
                "No specialized debugging "
                "tool is implemented for "
                f"{selected_tool}"
            )
        }

    # -----------------------------------------------------
    # Display important tool evidence
    # -----------------------------------------------------

    print("\nTOOL RESULT:")
    print(tool_result)

    return {
        "tool_route": route,
        "tool_result": tool_result
    }


# =========================================================
# NODE 7 — SOLUTION AGENT
# =========================================================

def generate_node(
    state: DebuggingState
):
    """
    Execute the dedicated Solution Agent.

    The Solution Agent receives the complete debugging state,
    including RAG context, specialist analysis, debugging-tool
    evidence, and previous verification feedback on retries.
    """

    print("\n" + "=" * 60)
    print("SOLUTION AGENT NODE")
    print("=" * 60)

    result = solution_agent(state)

    return {
        "solution": result.get(
            "solution",
            {}
        )
    }


# =========================================================
# NODE 8 — VERIFICATION AGENT
# =========================================================

def verify_node(
    state: DebuggingState
):
    """
    Execute the dedicated Verification Agent.

    The Verification Agent checks the generated solution
    against the original error, analysis, code, and actual
    debugging-tool evidence.
    """

    print("\n" + "=" * 60)
    print("VERIFICATION AGENT NODE")
    print("=" * 60)

    result = verification_agent(state)

    return {
        "verification": result.get(
            "verification",
            {}
        )
    }


# =========================================================
# NODE 9 — FINAL RESPONSE
# =========================================================

def final_node(
    state: DebuggingState
):
    """
    Build the final debugging response.
    """

    solution = state.get(
        "solution",
        {}
    )

    verification = state.get(
        "verification",
        {}
    )

    classification = state.get(
        "classification",
        {}
    )

    tool_route = state.get(
        "tool_route",
        {}
    )

    tool_result = state.get(
        "tool_result",
        {}
    )

    selected_agent = state.get(
        "selected_agent",
        "Unknown"
    )

    routing_reason = state.get(
        "routing_reason",
        ""
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    final_answer = f"""
==================================================
AI CODE DEBUGGING RESULT
==================================================

TECHNOLOGY
{classification.get("technology", "Unknown")}


SUPERVISOR SELECTED
{selected_agent}


ROUTING REASON
{routing_reason}


TOOL USED
{tool_route.get("tool", "Unknown")}


RETRY COUNT
{retry_count}


==================================================
PROBLEM
==================================================

{solution.get("problem", "N/A")}


==================================================
ROOT CAUSE
==================================================

{solution.get("root_cause", "N/A")}


==================================================
SOLUTION
==================================================

{solution.get("solution", "N/A")}


==================================================
CORRECTED CODE / COMMAND
==================================================

{solution.get("corrected_code", "N/A")}


==================================================
VERIFICATION
==================================================

Status:
{verification.get("status", "UNKNOWN")}

Confidence:
{verification.get("confidence", "UNKNOWN")}

Reason:
{verification.get("reason", "N/A")}


==================================================
VERIFICATION STEPS
==================================================

{solution.get("verification_steps", [])}


==================================================
PREVENTION
==================================================

{solution.get("prevention", "N/A")}


==================================================
DEBUGGING TOOL EVIDENCE
==================================================

{tool_result}
"""

    return {
        "final_answer": final_answer,

        "status": verification.get(
            "status",
            "UNKNOWN"
        )
    }


# =========================================================
# NODE 10 — RETRY
# =========================================================

def retry_node(
    state: DebuggingState
):
    """
    Increment retry count.

    The previous verification result is intentionally
    preserved in the state.

    This allows generate_node() to pass the verifier
    feedback back into the Solution Agent.
    """

    current_retry = state.get(
        "retry_count",
        0
    )

    new_retry_count = (
        current_retry + 1
    )

    verification = state.get(
        "verification",
        {}
    )

    print("\n" + "=" * 60)
    print("RETRY")
    print("=" * 60)

    print(
        f"Retry attempt: {new_retry_count}"
    )

    print(
        "Verification reason:",
        verification.get(
            "reason",
            "N/A"
        )
    )

    issues = verification.get(
        "issues",
        []
    )

    if issues:

        print(
            "Verification issues:"
        )

        for issue in issues:

            print(
                f"- {issue}"
            )

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # Return verification so it remains available
    # during the retry cycle.
    # -----------------------------------------------------

    return {
        "retry_count": new_retry_count,

        "verification": verification
    }


# =========================================================
# VERIFICATION ROUTER
# =========================================================

def verification_router(
    state: DebuggingState
):
    """
    Decide whether to:

    PASS  → final

    FAIL  → retry

    Maximum retry count = 2
    """

    verification = state.get(
        "verification",
        {}
    )

    status = str(
        verification.get(
            "status",
            "FAIL"
        )
    ).upper()

    retry_count = state.get(
        "retry_count",
        0
    )

    # =====================================================
    # SUCCESS
    # =====================================================

    if status == "PASS":

        print(
            "\nVerification PASSED."
        )

        return "final"

    # =====================================================
    # MAX RETRIES
    # =====================================================

    if retry_count >= 2:

        print(
            "\nMaximum retry limit reached."
        )

        return "final"

    # =====================================================
    # RETRY
    # =====================================================

    print(
        "\nVerification FAILED. "
        "Sending back for retry."
    )

    return "retry"


# =========================================================
# BUILD LANGGRAPH
# =========================================================

def build_debugging_graph():
    """
    Build the complete multi-agent debugging graph.
    """

    workflow = StateGraph(
        DebuggingState
    )

    # =====================================================
    # ADD MAIN NODES
    # =====================================================

    workflow.add_node(
        "classify",
        classify_node
    )

    workflow.add_node(
        "analyze",
        analyze_node
    )

    workflow.add_node(
        "rag",
        rag_node
    )

    workflow.add_node(
        "supervisor",
        supervisor_node
    )

    # =====================================================
    # ADD SPECIALIST AGENTS
    # =====================================================

    workflow.add_node(
        "python_agent",
        python_specialist_node
    )

    workflow.add_node(
        "sql_agent",
        sql_specialist_node
    )

    workflow.add_node(
        "postgresql_agent",
        postgresql_specialist_node
    )

    workflow.add_node(
        "docker_agent",
        docker_specialist_node
    )

    workflow.add_node(
        "airflow_agent",
        airflow_specialist_node
    )

    # =====================================================
    # ADD REMAINING NODES
    # =====================================================

    workflow.add_node(
        "debug_tool",
        debugging_tool_node
    )

    workflow.add_node(
        "solution_agent",
        generate_node
    )

    workflow.add_node(
        "verification_agent",
        verify_node
    )

    workflow.add_node(
        "retry",
        retry_node
    )

    workflow.add_node(
        "final",
        final_node
    )

    # =====================================================
    # INITIAL FLOW
    # =====================================================

    workflow.add_edge(
        START,
        "classify"
    )

    workflow.add_edge(
        "classify",
        "analyze"
    )

    workflow.add_edge(
        "analyze",
        "rag"
    )

    workflow.add_edge(
        "rag",
        "supervisor"
    )

    # =====================================================
    # SUPERVISOR → SPECIALIST ROUTING
    # =====================================================

    workflow.add_conditional_edges(
        "supervisor",
        specialist_router,
        {
            "python_agent":
                "python_agent",

            "sql_agent":
                "sql_agent",

            "postgresql_agent":
                "postgresql_agent",

            "docker_agent":
                "docker_agent",

            "airflow_agent":
                "airflow_agent"
        }
    )

    # =====================================================
    # SPECIALISTS → DEBUG TOOL
    # =====================================================

    workflow.add_edge(
        "python_agent",
        "debug_tool"
    )

    workflow.add_edge(
        "sql_agent",
        "debug_tool"
    )

    workflow.add_edge(
        "postgresql_agent",
        "debug_tool"
    )

    workflow.add_edge(
        "docker_agent",
        "debug_tool"
    )

    workflow.add_edge(
        "airflow_agent",
        "debug_tool"
    )

    # =====================================================
    # DEBUG TOOL → SOLUTION
    # =====================================================

    workflow.add_edge(
        "debug_tool",
        "solution_agent"
    )

    # =====================================================
    # SOLUTION → VERIFICATION
    # =====================================================

    workflow.add_edge(
        "solution_agent",
        "verification_agent"
    )

    # =====================================================
    # VERIFICATION → PASS / RETRY
    # =====================================================

    workflow.add_conditional_edges(
        "verification_agent",
        verification_router,
        {
            "final":
                "final",

            "retry":
                "retry"
        }
    )

    # =====================================================
    # RETRY → ANALYSIS
    # =====================================================

    workflow.add_edge(
        "retry",
        "analyze"
    )

    # =====================================================
    # FINAL → END
    # =====================================================

    workflow.add_edge(
        "final",
        END
    )

    # =====================================================
    # COMPILE
    # =====================================================

    return workflow.compile()
from pathlib import Path
import html
import json

import streamlit as st

from agent.graph import build_debugging_graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DebugAI | Developer Debugging Platform",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSS_FILE = BASE_DIR / "frontend" / "style.css"

# If style.css is next to app.py instead, this fallback supports it.
if not CSS_FILE.exists():
    CSS_FILE = BASE_DIR / "style.css"


# ============================================================
# LOAD CSS
# IMPORTANT:
# Use st.html() so the CSS/HTML is not parsed as Markdown.
# ============================================================

if CSS_FILE.exists():
    css = CSS_FILE.read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")
else:
    st.error(f"style.css was not found: {CSS_FILE}")


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "result": None,
    "history": [],
    "error_input": "",
    "code_input": "",
    "show_history": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPERS
# ============================================================

def render_html(content: str):
    """
    Render real HTML.

    Do not replace this with st.markdown().
    This prevents <div>, <span>, etc. from appearing as text.
    """
    st.html(content.strip())


def safe_text(value, default="Not available"):
    if value is None:
        return default

    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
        )

    value = str(value).strip()
    return value if value else default


def esc(value, default="Not available"):
    return html.escape(
        safe_text(value, default),
        quote=True,
    )


def as_dict(value):
    return value if isinstance(value, dict) else {}


def first_value(data, keys, default="Not available"):
    data = as_dict(data)

    for key in keys:
        value = data.get(key)

        if value not in (None, "", [], {}):
            return value

    return default


def verification_status(verification):
    status = as_dict(verification).get("status", "UNKNOWN")

    if isinstance(status, bool):
        return "PASS" if status else "FAIL"

    status = str(status).upper().strip()

    if status in {
        "PASS",
        "PASSED",
        "SUCCESS",
        "VERIFIED",
        "TRUE",
    }:
        return "PASS"

    return "FAIL"


def extract_result_fields(result):
    """
    Normalize the LangGraph result for the dashboard.
    """

    result = as_dict(result)

    classification = as_dict(
        result.get("classification")
    )

    analysis = as_dict(
        result.get("analysis")
    )

    solution = as_dict(
        result.get("solution")
    )

    verification = as_dict(
        result.get("verification")
    )

    tool_result = as_dict(
        result.get("tool_result")
    )

    # RAG compatibility: graph.py returns rag_context and
    # retrieved_documents, while the original UI expected
    # knowledge and documents.
    knowledge = result.get(
        "rag_context",
        result.get("knowledge", ""),
    )

    documents = result.get(
        "retrieved_documents",
        result.get("documents", []),
    )

    if not isinstance(documents, list):
        documents = []

    # ------------------------------------------------------------
    # PostgreSQL specialized debugging data
    # ------------------------------------------------------------
    #
    # The PostgreSQL agent stores its database investigation under
    # "postgresql_debugging". Depending on the graph/tool wiring,
    # it may appear directly in tool_result or nested under it.
    # Normalize both possibilities here so the UI can render it.
    postgresql_debugging = as_dict(
        tool_result.get("postgresql_debugging")
    )

    if not postgresql_debugging:
        # Some graph implementations may return the debugging
        # payload directly as the tool result.
        if any(
            key in tool_result
            for key in (
                "schema",
                "column_search",
                "join_analysis",
                "sql_validation",
            )
        ):
            postgresql_debugging = tool_result

    return {
        "technology": first_value(
            classification,
            ["technology", "tech"],
            "Unknown",
        ),

        "error_type": first_value(
            classification,
            ["error_type", "errorType", "type"],
            "Unknown",
        ),

        "category": first_value(
            classification,
            ["category"],
            "Unknown",
        ),

        "problem": first_value(
            analysis,
            ["problem", "issue"],
            first_value(
                solution,
                ["problem"],
                "No problem description returned.",
            ),
        ),

        "root_cause": first_value(
            analysis,
            ["root_cause", "rootCause"],
            first_value(
                solution,
                ["root_cause", "rootCause"],
                "No root cause returned.",
            ),
        ),

        "solution": first_value(
            solution,
            [
                "solution",
                "explanation",
                "recommended_fix",
            ],
            "No solution returned.",
        ),

        "corrected_code": first_value(
            solution,
            [
                "corrected_code",
                "correctedCode",
                "code",
            ],
            "No corrected code returned.",
        ),

        "verification_steps": solution.get(
            "verification_steps",
            [],
        ),

        "prevention": solution.get(
            "prevention",
            "No prevention guidance returned.",
        ),

        "knowledge": knowledge,

        "documents": documents,

        "analysis": analysis,

        "tool_result": tool_result,

        # PostgreSQL-specific investigation results
        "postgresql_debugging": postgresql_debugging,
        "postgresql_schema": as_dict(
            postgresql_debugging.get("schema")
        ),
        "postgresql_column_search": as_dict(
            postgresql_debugging.get("column_search")
        ),
        "postgresql_join_analysis": as_dict(
            postgresql_debugging.get("join_analysis")
        ),
        "postgresql_sql_validation": as_dict(
            postgresql_debugging.get("sql_validation")
        ),
        "postgresql_corrected_sql": (
            postgresql_debugging.get(
                "corrected_sql",
                "",
            )
        ),
        "postgresql_evidence": postgresql_debugging.get(
            "evidence",
            [],
        ),

        "solution_data": solution,

        "verification": verification,

        "retry_count": result.get(
            "retry_count",
            0,
        ),

        # REAL LangGraph node execution order captured by run_pipeline().
        "execution_trace": result.get(
            "_execution_trace",
            [],
        ),
    }



def render_agent_evidence_flow(fields):
    """Render the real LangGraph execution and accumulated evidence."""

    trace = fields.get("execution_trace", [])
    result_state = st.session_state.get("result") or {}

    technology = safe_text(fields.get("technology"), "Unknown")
    error_type = safe_text(fields.get("error_type"), "Unknown")
    documents = fields.get("documents", [])
    verification = as_dict(fields.get("verification"))
    tool_result = as_dict(fields.get("tool_result"))
    solution_data = as_dict(fields.get("solution_data"))
    pg_evidence = fields.get("postgresql_evidence", [])

    selected_agent = result_state.get(
        "selected_agent",
        "Specialist Agent",
    )
    routing_reason = result_state.get(
        "routing_reason",
        "Routing decision stored in DebuggingState.",
    )

    verification_result = verification_status(verification)

    render_html(f"""
    <div class="evidence-flow-shell">
        <div class="evidence-flow-header">
            <div>
                <div class="section-kicker">MULTI-AGENT EVIDENCE FLOW</div>
                <h2>Evidence flowing through the debugging agents</h2>
                <p>
                    The sequence below is captured from the real LangGraph
                    stream and the evidence comes from the shared DebuggingState.
                </p>
            </div>
            <div class="flow-live-badge">
                <span class="online-dot"></span>
                REAL LANGGRAPH TRACE
            </div>
        </div>

        <div class="flow-summary-grid">
            <div class="flow-summary">
                <div class="flow-summary-label">NODES EXECUTED</div>
                <div class="flow-summary-value">{esc(len(trace))}</div>
                <div class="flow-summary-meta">Captured from graph.stream()</div>
            </div>
            <div class="flow-summary">
                <div class="flow-summary-label">RAG SOURCES</div>
                <div class="flow-summary-value">{esc(len(documents))}</div>
                <div class="flow-summary-meta">Retrieved knowledge documents</div>
            </div>
            <div class="flow-summary">
                <div class="flow-summary-label">SPECIALIST</div>
                <div class="flow-summary-value">{esc(selected_agent)}</div>
                <div class="flow-summary-meta">Supervisor routing decision</div>
            </div>
            <div class="flow-summary">
                <div class="flow-summary-label">VERIFICATION</div>
                <div class="flow-summary-value">{esc(verification_result)}</div>
                <div class="flow-summary-meta">Final verification stage</div>
            </div>
        </div>
    </div>
    """)

    def ran(*names):
        lowered = [str(x).lower() for x in trace]
        return any(
            any(name.lower() in item for item in lowered)
            for name in names
        )

    stages = [
        (
            "01", "Error Classifier",
            ran("classifier", "classification"),
            f"{technology} / {error_type}",
            "Error message + source code",
            f"Technology: {technology}<br>Error type: {error_type}",
        ),
        (
            "02", "RAG Agent",
            ran("rag", "retrieval", "knowledge"),
            f"{len(documents)} document(s) retrieved",
            f"{technology} / {error_type}",
            "Relevant debugging knowledge added to context",
        ),
        (
            "03", "Supervisor Agent",
            ran("supervisor", "routing", "route"),
            f"Route → {selected_agent}",
            "Classification + error + code",
            esc(routing_reason),
        ),
        (
            "04", str(selected_agent),
            ran(
                "postgresql_agent", "python_agent", "sql_agent",
                "docker_agent", "airflow_agent", "specialist"
            ),
            "Technology-specific investigation",
            "Supervisor routing decision",
            "Specialist diagnosis and evidence request",
        ),
        (
            "05", "Debugging Tool",
            ran(
                "tool", "debugging_tool",
                "execute_postgresql_tool",
                "execute_python_tool",
                "execute_sql_tool",
            ),
            tool_result.get("tool_name", "Specialized tool"),
            "Specialist diagnosis",
            "Schema / runtime / environment evidence collected",
        ),
        (
            "06", "Solution Agent",
            ran("solution", "solution_agent", "generate"),
            "Diagnosis + RAG + tool evidence",
            "Accumulated debugging evidence",
            "Corrected code and recommended fix generated",
        ),
        (
            "07", "Verification Agent",
            ran("verification", "verification_agent"),
            f"Status: {verification_result}",
            "Generated solution",
            safe_text(
                verification.get(
                    "reason",
                    "Verification evidence available."
                )
            ),
        ),
        (
            "08", "Final Response",
            bool(trace),
            "Verified solution",
            "Complete DebuggingState",
            "Final debugging result returned to the UI",
        ),
    ]

    for index, (number, title, complete, evidence, source, output) in enumerate(stages):
        status = "COMPLETE" if complete else "NOT OBSERVED"
        css = "flow-complete" if complete else "flow-muted"

        render_html(f"""
        <div class="agent-flow-row">
            <div class="agent-node {css}">
                <div class="agent-node-top">
                    <div class="agent-node-number">{number}</div>
                    <div>
                        <div class="agent-node-title">{esc(title)}</div>
                        <div class="agent-node-status">{status}</div>
                    </div>
                </div>

                <div class="agent-node-body">
                    <div class="flow-field">
                        <span>INPUT</span>
                        <strong>{esc(source)}</strong>
                    </div>
                    <div class="flow-field evidence">
                        <span>EVIDENCE</span>
                        <strong>{esc(evidence)}</strong>
                    </div>
                    <div class="flow-field">
                        <span>OUTPUT</span>
                        <strong>{esc(output)}</strong>
                    </div>
                </div>
            </div>
        </div>
        """)

        if index < len(stages) - 1:
            render_html("""
            <div class="flow-arrow">
                <span>↓</span>
                <span class="flow-arrow-label">EVIDENCE HANDOFF</span>
            </div>
            """)

    if technology.lower() == "postgresql":
        pg = fields.get("postgresql_debugging", {})
        pg_schema = fields.get("postgresql_schema", {})
        pg_column = as_dict(pg.get("column"))
        pg_matches = fields.get(
            "postgresql_column_search", {}
        ).get("matches", [])
        pg_validation = fields.get(
            "postgresql_sql_validation", {}
        )
        corrected_sql = fields.get(
            "postgresql_corrected_sql", ""
        )

        render_html(f"""
        <div class="evidence-chain">
            <div class="section-kicker">DATABASE EVIDENCE CHAIN</div>
            <h3>PostgreSQL proof behind the correction</h3>

            <div class="evidence-chain-grid">
                <div class="evidence-proof">
                    <div class="proof-label">1 · SCHEMA</div>
                    <div class="proof-value">
                        {esc(pg.get("table_name", "Unknown table"))}
                    </div>
                    <div class="proof-meta">
                        {len(pg_schema.get("columns", []))} columns inspected
                    </div>
                </div>

                <div class="evidence-proof">
                    <div class="proof-label">2 · COLUMN CHECK</div>
                    <div class="proof-value">
                        {esc(pg_column.get("column", pg.get("column_name", "Unknown")))}
                    </div>
                    <div class="proof-meta">
                        {"Column exists" if pg_column.get("exists") else "Column missing"}
                    </div>
                </div>

                <div class="evidence-proof">
                    <div class="proof-label">3 · DISCOVERY</div>
                    <div class="proof-value">{len(pg_matches)} match(es)</div>
                    <div class="proof-meta">Candidate columns found</div>
                </div>

                <div class="evidence-proof">
                    <div class="proof-label">4 · VALIDATION</div>
                    <div class="proof-value">
                        {"PASS" if pg_validation.get("success") else "FAIL"}
                    </div>
                    <div class="proof-meta">Corrected SQL execution</div>
                </div>
            </div>
        </div>
        """)

        if corrected_sql:
            with st.expander(
                "View corrected SQL produced from database evidence"
            ):
                st.code(corrected_sql, language="sql")

    render_html("""
    <div class="trace-note">
        <strong>Demo note:</strong>
        node order is captured from the real LangGraph stream.
        The evidence shown in each stage is read from the accumulated
        DebuggingState returned by the graph.
    </div>
    """)


def run_pipeline():
    error_message = st.session_state.error_input.strip()
    code = st.session_state.code_input.strip()

    if not error_message:
        st.warning("Please enter an error message.")
        return

    try:
        with st.spinner("Analyzing error and generating solution..."):

            graph = build_debugging_graph()

            # --------------------------------------------------------
            # Execute the LangGraph as a stream so we can capture the
            # REAL node/agent execution path for the dashboard.
            # --------------------------------------------------------
            result = {}
            execution_trace = []

            for update in graph.stream(
                {
                    "error_message": error_message,
                    "code": code,
                    "retry_count": 0,
                },
                stream_mode="updates",
            ):
                if not isinstance(update, dict):
                    continue

                # Each top-level key is the actual LangGraph node
                # that emitted an update.
                for node_name, node_update in update.items():

                    if node_name not in execution_trace:
                        execution_trace.append(
                            str(node_name)
                        )

                    if isinstance(node_update, dict):
                        result.update(node_update)

            # Keep the real execution trace alongside the final state.
            result["_execution_trace"] = execution_trace

        st.session_state.result = result

        fields = extract_result_fields(result)

        status = verification_status(
            fields["verification"]
        )

        # For PostgreSQL, the specialized SQL validation is a
        # stronger signal than the generic verification stage.
        pg_validation = fields.get(
            "postgresql_sql_validation",
            {}
        )

        if (
            fields.get("technology", "").lower()
            == "postgresql"
            and pg_validation
        ):
            status = (
                "PASS"
                if pg_validation.get("success")
                else "FAIL"
            )

        st.session_state.history.insert(
            0,
            {
                "technology": fields["technology"],
                "error_type": fields["error_type"],
                "tool": fields["tool_result"].get(
                    "tool_name",
                    "Unknown",
                ),
                "status": status,
            },
        )

        st.session_state.history = (
            st.session_state.history[:20]
        )

        st.success(
            "Debugging completed successfully."
        )

    except Exception as exc:

        message = str(exc)

        if (
            "429" in message
            or "RESOURCE_EXHAUSTED" in message
            or "quota" in message.lower()
        ):
            st.error(
                "AI model quota has been exceeded. "
                "Please wait and retry, or use a model/API key "
                "with available quota."
            )
        else:
            st.error(
                "The debugging pipeline failed."
            )

        with st.expander("Technical details"):
            st.exception(exc)


def load_demo(kind):
    demos = {
        "Python": (
            "ModuleNotFoundError: No module named 'pandas'",
            "import pandas as pd\n\nprint(pd.__version__)",
        ),

        "PostgreSQL": (
            'psycopg2.errors.UndefinedColumn: '
            'column "customer_name" does not exist',
            "SELECT customer_name, order_id\nFROM orders;",
        ),

        "Docker": (
            "Cannot connect to the Docker daemon.\n"
            "Is the docker daemon running?",
            "docker ps",
        ),

        "Airflow": (
            "Broken DAG: Failed to import DAG file",
            """from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="broken_dag",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    pass""",
        ),

        "SQL": (
            "ERROR: column customer_name does not exist",
            "SELECT customer_name, order_id FROM orders;",
        ),
    }

    error_value, code_value = demos[kind]

    st.session_state.error_input = error_value
    st.session_state.code_input = code_value
    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">

            <div class="brand-mark">
                &lt;/&gt;
            </div>

            <div>
                <div class="brand-name">
                    Debug<span>AI</span>
                </div>

                <div class="brand-subtitle">
                    Developer Debugging Platform
                </div>
            </div>

        </div>

        <div class="sidebar-divider"></div>

        <div class="side-section-title">
            WORKSPACE
        </div>
        """
    )

    if st.button(
        "⌁  Debug Console",
        width="stretch",
        key="nav_console",
    ):
        st.session_state.show_history = False

    if st.button(
        "◷  Analysis History",
        width="stretch",
        key="nav_history",
    ):
        st.session_state.show_history = True

    render_html(
        """
        <div class="side-section-title">
            SUPPORTED TECHNOLOGIES
        </div>

        <div class="tech-row">
            <span class="tech-icon python">PY</span>
            <span>Python</span>
        </div>

        <div class="tech-row">
            <span class="tech-icon sql">SQL</span>
            <span>SQL</span>
        </div>

        <div class="tech-row">
            <span class="tech-icon postgres">PG</span>
            <span>PostgreSQL</span>
        </div>

        <div class="tech-row">
            <span class="tech-icon docker">DK</span>
            <span>Docker</span>
        </div>

        <div class="tech-row">
            <span class="tech-icon airflow">AF</span>
            <span>Airflow</span>
        </div>

        <div class="side-section-title quick-title">
            QUICK TEST
        </div>
        """
    )

    for demo_name in [
        "Python",
        "SQL",
        "PostgreSQL",
        "Docker",
        "Airflow",
    ]:
        if st.button(
            f"Test {demo_name}",
            width="stretch",
            key=f"demo_{demo_name.lower()}",
        ):
            load_demo(demo_name)

    render_html(
        """
        <div class="sidebar-status">

            <div class="status-caption">
                ENGINE STATUS
            </div>

            <div class="status-online">
                <span class="online-dot"></span>
                LangGraph engine online
            </div>

            <div class="status-stack">
                RAG&nbsp;&nbsp;•&nbsp;&nbsp;TOOLS&nbsp;&nbsp;•&nbsp;&nbsp;LLM
            </div>

        </div>
        """
    )


# ============================================================
# TOP BAR
# ============================================================

render_html(
    """
    <div class="top-bar">

        <div class="breadcrumb">
            Workspace
            <span>/</span>
            <strong>Debug Console</strong>
        </div>

        <div class="top-actions">

            <div class="online-badge">
                <span class="online-dot"></span>
                ENGINE ONLINE
            </div>

            <div class="engine-badge">
                LANGGRAPH
            </div>

        </div>

    </div>
    """
)


# ============================================================
# HISTORY VIEW
# ============================================================

if st.session_state.show_history:

    render_html(
        """
        <div class="page-hero compact">

            <div class="hero-eyebrow">
                DEBUG HISTORY
            </div>

            <h1>Analysis History</h1>

            <p>
                Review recent debugging sessions and their verification status.
            </p>

        </div>
        """
    )

    if not st.session_state.history:

        render_html(
            """
            <div class="empty-card">

                <div class="empty-icon">
                    ◷
                </div>

                <div class="empty-title">
                    No debugging runs yet
                </div>

                <div class="empty-text">
                    Run a debugging session from the console
                    and it will appear here.
                </div>

            </div>
            """
        )

    else:

        for index, item in enumerate(
            st.session_state.history,
            start=1,
        ):

            status = str(
                item.get("status", "UNKNOWN")
            ).upper()

            status_class = (
                "history-pass"
                if status == "PASS"
                else "history-fail"
            )

            render_html(
                f"""
                <div class="history-card">

                    <div class="history-index">
                        #{index:02d}
                    </div>

                    <div class="history-main">

                        <div class="history-tech">
                            {esc(item.get("technology"))}
                        </div>

                        <div class="history-error">
                            {esc(item.get("error_type"))}
                        </div>

                    </div>

                    <div class="history-tool">
                        {esc(item.get("tool"))}
                    </div>

                    <div class="{status_class}">
                        {esc(status)}
                    </div>

                </div>
                """
            )

else:

    # ========================================================
    # HERO
    # ========================================================

    render_html(
        """
        <div class="hero-grid">

            <div class="hero-copy">

                <div class="hero-eyebrow">
                    AI-POWERED DEBUGGING
                </div>

                <h1>
                    Find the problem.
                    <span>Fix the code.</span>
                </h1>

                <p>
                    Diagnose software errors, inspect source code,
                    retrieve relevant knowledge and receive a
                    verified solution from your debugging agent.
                </p>

            </div>

            <div class="engine-card">

                <div class="engine-card-top">

                    <span class="online-dot"></span>

                    <span>
                        DEBUG ENGINE
                    </span>

                </div>

                <div class="engine-card-title">
                    ONLINE
                </div>

                <div class="engine-card-stack">
                    LANGGRAPH&nbsp;&nbsp;•&nbsp;&nbsp;
                    RAG&nbsp;&nbsp;•&nbsp;&nbsp;
                    SPECIALIZED TOOLS
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # DASHBOARD METRICS
    # ========================================================

    total_runs = len(
        st.session_state.history
    )

    verified_runs = sum(
        1
        for item in st.session_state.history
        if item.get("status") == "PASS"
    )

    failed_runs = sum(
        1
        for item in st.session_state.history
        if item.get("status") == "FAIL"
    )

    metric_cols = st.columns(4)

    metrics = [
        (
            "DEBUG RUNS",
            total_runs,
            "Total sessions",
            "blue",
        ),
        (
            "VERIFIED",
            verified_runs,
            "Successful checks",
            "green",
        ),
        (
            "FAILED",
            failed_runs,
            "Needs attention",
            "red",
        ),
        (
            "ENGINE",
            "ONLINE",
            "LangGraph ready",
            "purple",
        ),
    ]

    for column, metric in zip(
        metric_cols,
        metrics,
    ):

        label, value, meta, tone = metric

        with column:

            render_html(
                f"""
                <div class="metric-card {tone}">

                    <div class="metric-label">
                        {esc(label)}
                    </div>

                    <div class="metric-value">
                        {esc(value)}
                    </div>

                    <div class="metric-meta">
                        {esc(meta)}
                    </div>

                </div>
                """
            )


    # ========================================================
    # DEBUG CONSOLE
    # ========================================================

    render_html(
        """
        <div class="console-header">

            <div>

                <div class="section-kicker">
                    DEBUG CONSOLE
                </div>

                <h2>
                    What are you debugging?
                </h2>

                <p>
                    Paste the error and the related
                    source code, SQL query or command.
                </p>

            </div>

            <div class="ready-badge">
                <span class="ready-dot"></span>
                READY
            </div>

        </div>
        """
    )


    input_left, input_right = st.columns(
        2,
        gap="large",
    )


    # ========================================================
    # ERROR INPUT
    # ========================================================

    with input_left:

        render_html(
            """
            <div class="editor-shell">

                <div class="editor-header">

                    <div>
                        <div class="editor-title">
                            ERROR MESSAGE
                        </div>

                        <div class="editor-subtitle">
                            Runtime / compiler / database error
                        </div>
                    </div>

                    <div class="editor-tag error-tag">
                        ERROR
                    </div>

                </div>

            </div>
            """
        )

        st.text_area(
            "Error message",
            key="error_input",
            height=240,
            label_visibility="collapsed",
            placeholder=(
                "Paste the complete error message here...\n\n"
                "Example:\n"
                "ModuleNotFoundError: No module named 'pandas'"
            ),
        )


    # ========================================================
    # CODE INPUT
    # ========================================================

    with input_right:

        render_html(
            """
            <div class="editor-shell">

                <div class="editor-header">

                    <div>
                        <div class="editor-title">
                            SOURCE CODE / COMMAND
                        </div>

                        <div class="editor-subtitle">
                            Python / SQL / Docker / Airflow
                        </div>
                    </div>

                    <div class="editor-tag code-tag">
                        CODE
                    </div>

                </div>

            </div>
            """
        )

        st.text_area(
            "Source code",
            key="code_input",
            height=240,
            label_visibility="collapsed",
            placeholder=(
                "Paste the related source code, SQL query, "
                "Docker command or Airflow code here..."
            ),
        )


    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    st.write("")

    run_col, clear_col = st.columns(
        [5, 1],
        gap="medium",
    )

    with run_col:

        if st.button(
            "▶  RUN AI DEBUGGING",
            width="stretch",
            type="primary",
            key="run_debugging",
        ):
            run_pipeline()

    with clear_col:

        if st.button(
            "CLEAR",
            width="stretch",
            key="clear_debugging",
        ):
            st.session_state.error_input = ""
            st.session_state.code_input = ""
            st.session_state.result = None
            st.rerun()


    # ========================================================
    # RESULTS
    # ========================================================

    result = st.session_state.result

    if result:

        fields = extract_result_fields(
            result
        )

        technology = fields["technology"]
        error_type = fields["error_type"]
        tool_name = fields["tool_result"].get(
            "tool_name",
            "Unknown",
        )
        retry_count = fields["retry_count"]

        verification = fields["verification"]
        verification_result = verification_status(
            verification
        )


        # ----------------------------------------------------
        # RESULT HEADER
        # ----------------------------------------------------

        render_html(
            """
            <div class="results-header">

                <div>

                    <div class="section-kicker">
                        ANALYSIS COMPLETE
                    </div>

                    <h2>
                        Debugging Result
                    </h2>

                </div>

                <div class="completed-badge">
                    ✓ COMPLETED
                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # RESULT SUMMARY
        # ----------------------------------------------------

        result_cols = st.columns(4)

        result_metrics = [
            (
                "TECHNOLOGY",
                technology,
                "Detected platform",
            ),
            (
                "ERROR TYPE",
                error_type,
                "Classified error",
            ),
            (
                "SPECIALIZED TOOL",
                tool_name,
                "Evidence source",
            ),
            (
                "NODES EXECUTED",
                len(fields.get("execution_trace", [])),
                "Real LangGraph nodes",
            ),
        ]

        for column, item in zip(
            result_cols,
            result_metrics,
        ):

            label, value, meta = item

            with column:

                render_html(
                    f"""
                    <div class="result-metric">

                        <div class="result-metric-label">
                            {esc(label)}
                        </div>

                        <div class="result-metric-value">
                            {esc(value)}
                        </div>

                        <div class="result-metric-meta">
                            {esc(meta)}
                        </div>

                    </div>
                    """
                )


        # ----------------------------------------------------
        # VERIFICATION BANNER
        # ----------------------------------------------------

        if verification_result == "PASS":

            render_html(
                """
                <div class="verification-banner pass">

                    <div class="verification-icon">
                        ✓
                    </div>

                    <div>

                        <div class="verification-title">
                            Verification Passed
                        </div>

                        <div class="verification-text">
                            The generated solution passed the
                            verification stage.
                        </div>

                    </div>

                </div>
                """
            )

        else:

            render_html(
                """
                <div class="verification-banner fail">

                    <div class="verification-icon">
                        !
                    </div>

                    <div>

                        <div class="verification-title">
                            Verification Requires Attention
                        </div>

                        <div class="verification-text">
                            Review the generated solution and
                            verification evidence.
                        </div>

                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # RESULT TABS
        # ----------------------------------------------------

        is_postgresql = (
            technology.lower().strip()
            == "postgresql"
        )

        # Execution Trace is always available and is populated from
        # the actual LangGraph stream -- not a hard-coded/static list.
        tab_labels = [
            "Agent Evidence Flow",
            "AI Solution",
            "Tool Evidence",
            "RAG Knowledge",
            "Code Analysis",
            "Verification",
            "Execution Trace",
        ]

        if is_postgresql:
            tab_labels.append(
                "PostgreSQL Investigation"
            )

        tabs = st.tabs(tab_labels)


        # ====================================================
        # AGENT EVIDENCE FLOW
        # ====================================================

        with tabs[0]:
            render_agent_evidence_flow(fields)

        # ====================================================
        # AI SOLUTION
        # ====================================================

        with tabs[1]:

            render_html(
                """
                <div class="result-panel-heading">
                    <div class="result-panel-title">
                        AI Generated Solution
                    </div>

                    <div class="result-panel-description">
                        Diagnosis, root cause and recommended fix.
                    </div>
                </div>
                """
            )

            render_html(
                f"""
                <div class="answer-card">

                    <div class="answer-label">
                        PROBLEM
                    </div>

                    <div class="answer-text">
                        {esc(fields["problem"])}
                    </div>

                </div>
                """
            )

            render_html(
                f"""
                <div class="answer-card">

                    <div class="answer-label">
                        ROOT CAUSE
                    </div>

                    <div class="answer-text">
                        {esc(fields["root_cause"])}
                    </div>

                </div>
                """
            )

            render_html(
                f"""
                <div class="answer-card">

                    <div class="answer-label">
                        RECOMMENDED FIX
                    </div>

                    <div class="answer-text">
                        {esc(fields["solution"])}
                    </div>

                </div>
                """
            )

            render_html(
                """
                <div class="code-result-title">
                    CORRECTED CODE / COMMAND
                </div>
                """
            )

            st.code(
                safe_text(
                    fields["corrected_code"],
                    "No corrected code returned.",
                ),
                language="text",
            )

            steps = fields["verification_steps"]

            render_html(
                """
                <div class="code-result-title">
                    VERIFICATION STEPS
                </div>
                """
            )

            if isinstance(steps, list):

                for index, step in enumerate(
                    steps,
                    start=1,
                ):

                    st.markdown(
                        f"**{index}.** {safe_text(step)}"
                    )

            else:

                st.write(
                    safe_text(steps)
                )

            render_html(
                f"""
                <div class="answer-card">

                    <div class="answer-label">
                        PREVENTION
                    </div>

                    <div class="answer-text">
                        {esc(fields["prevention"])}
                    </div>

                </div>
                """
            )


        # ====================================================
        # TOOL EVIDENCE
        # ====================================================

        with tabs[1]:

            render_html(
                """
                <div class="result-panel-heading">

                    <div class="result-panel-title">
                        Specialized Tool Evidence
                    </div>

                    <div class="result-panel-description">
                        Evidence collected by the
                        technology-specific debugging tool.
                    </div>

                </div>
                """
            )

            st.json(
                fields["tool_result"]
            )


        # ====================================================
        # RAG KNOWLEDGE
        # ====================================================

        with tabs[3]:

            render_html(
                """
                <div class="result-panel-heading">

                    <div class="result-panel-title">
                        Retrieved Knowledge
                    </div>

                    <div class="result-panel-description">
                        Relevant information retrieved from
                        the debugging knowledge base.
                    </div>

                </div>
                """
            )

            knowledge = fields["knowledge"]
            documents = fields["documents"]

            if knowledge or documents:
                render_html(
                    f"""
                    <div class="answer-card">
                        <div class="answer-label">
                            RAG RETRIEVAL STATUS
                        </div>
                        <div class="answer-text">
                            ✓ {len(documents)} relevant knowledge
                            document(s) retrieved.
                        </div>
                    </div>
                    """
                )
            else:
                st.info(
                    "No additional knowledge was retrieved."
                )

            if knowledge:
                render_html(
                    """
                    <div class="code-result-title">
                        RETRIEVED RAG CONTEXT
                    </div>
                    """
                )
                st.markdown(str(knowledge))

            if documents:
                with st.expander(
                    f"View retrieved documents ({len(documents)})",
                    expanded=True,
                ):
                    for index, document in enumerate(
                        documents,
                        start=1,
                    ):
                        st.markdown(f"### Document {index}")

                        if isinstance(document, dict):
                            source = document.get(
                                "source",
                                document.get(
                                    "metadata", {}
                                ).get("source", "Unknown source")
                            )
                            technology = document.get(
                                "technology",
                                document.get(
                                    "metadata", {}
                                ).get("technology", "Unknown")
                            )
                            category = document.get(
                                "category",
                                document.get(
                                    "metadata", {}
                                ).get("category", "Unknown")
                            )
                            content = document.get(
                                "content",
                                document.get(
                                    "text",
                                    document.get(
                                        "page_content",
                                        document
                                    )
                                )
                            )

                            st.markdown(
                                f"**Source:** `{safe_text(source)}`"
                            )
                            st.caption(
                                f"Technology: {safe_text(technology)} | "
                                f"Category: {safe_text(category)}"
                            )

                            if isinstance(content, (dict, list)):
                                st.json(content)
                            else:
                                st.markdown(str(content))
                        else:
                            st.write(safe_text(document))


        # ====================================================
        # CODE ANALYSIS
        # ====================================================

        with tabs[4]:

            render_html(
                """
                <div class="result-panel-heading">

                    <div class="result-panel-title">
                        Code Analysis
                    </div>

                    <div class="result-panel-description">
                        AI analysis generated before the
                        specialized debugging tool.
                    </div>

                </div>
                """
            )

            st.json(
                fields["analysis"]
            )


        # ====================================================
        # VERIFICATION
        # ====================================================

        with tabs[5]:

            render_html(
                f"""
                <div class="verification-detail">

                    <div class="verification-detail-status">
                        {esc(verification_result)}
                    </div>

                    <div class="verification-detail-title">
                        Verification Result
                    </div>

                    <div class="verification-detail-text">
                        {esc(
                            verification.get(
                                "reason",
                                "No verification reason available.",
                            )
                        )}
                    </div>

                </div>
                """
            )

            with st.expander(
                "View complete verification data"
            ):

                st.json(
                    verification
                )


        # ====================================================
        # REAL MULTI-AGENT / LANGGRAPH EXECUTION TRACE
        # ====================================================

        with tabs[6]:

            execution_trace = fields.get(
                "execution_trace",
                []
            )

            render_html(
                """
                <div class="result-panel-heading">
                    <div class="result-panel-title">
                        Multi-Agent Execution Trace
                    </div>
                    <div class="result-panel-description">
                        Actual LangGraph nodes that executed for this
                        debugging request, captured from the graph stream.
                    </div>
                </div>
                """
            )

            if execution_trace:

                render_html(
                    f"""
                    <div class="answer-card">
                        <div class="answer-label">
                            EXECUTION STATUS
                        </div>
                        <div class="answer-text">
                            <strong>{esc(len(execution_trace))}</strong>
                            graph nodes executed in sequence.
                        </div>
                    </div>
                    """
                )

                for index, node_name in enumerate(
                    execution_trace,
                    start=1,
                ):

                    # The name shown here is the real graph node name.
                    render_html(
                        f"""
                        <div class="answer-card">
                            <div class="answer-label">
                                STEP {index:02d}
                            </div>
                            <div class="answer-text">
                                ✓ {esc(node_name)}
                            </div>
                        </div>
                        """
                    )

                with st.expander(
                    "View raw execution trace"
                ):

                    st.json(
                        {
                            "execution_trace": execution_trace
                        }
                    )

            else:

                st.warning(
                    "No LangGraph execution trace was captured."
                )


        # ====================================================
        # POSTGRESQL INVESTIGATION
        # ====================================================

        if is_postgresql:

            pg = fields.get(
                "postgresql_debugging",
                {}
            )

            pg_schema = fields.get(
                "postgresql_schema",
                {}
            )

            pg_column_search = fields.get(
                "postgresql_column_search",
                {}
            )

            pg_join = fields.get(
                "postgresql_join_analysis",
                {}
            )

            pg_validation = fields.get(
                "postgresql_sql_validation",
                {}
            )

            pg_corrected_sql = fields.get(
                "postgresql_corrected_sql",
                ""
            )

            pg_evidence = fields.get(
                "postgresql_evidence",
                []
            )

            with tabs[7]:

                render_html(
                    """
                    <div class="result-panel-heading">
                        <div class="result-panel-title">
                            PostgreSQL Investigation
                        </div>
                        <div class="result-panel-description">
                            Live database inspection, root-cause evidence,
                            JOIN analysis and corrected SQL validation.
                        </div>
                    </div>
                    """
                )

                # ------------------------------------------------
                # Investigation status cards
                # ------------------------------------------------

                pg_connection = as_dict(
                    pg.get("connection")
                )

                pg_table = as_dict(
                    pg.get("table")
                )

                pg_column = as_dict(
                    pg.get("column")
                )

                connection_status = (
                    "CONNECTED"
                    if pg_connection.get("connected")
                    else "FAILED"
                )

                table_status = (
                    "FOUND"
                    if pg_table.get("exists")
                    else "NOT FOUND"
                )

                column_status = (
                    "FOUND"
                    if pg_column.get("exists")
                    else "MISSING"
                )

                validation_status = (
                    "PASS"
                    if pg_validation.get("success")
                    else "FAIL"
                )

                pg_cols = st.columns(4)

                pg_metrics = [
                    (
                        "DATABASE",
                        connection_status,
                        "PostgreSQL connection",
                    ),
                    (
                        "TABLE",
                        table_status,
                        safe_text(
                            pg.get(
                                "table_name",
                                "Detected table",
                            )
                        ),
                    ),
                    (
                        "MISSING COLUMN",
                        column_status,
                        safe_text(
                            pg.get(
                                "column_name",
                                "Detected column",
                            )
                        ),
                    ),
                    (
                        "SQL VALIDATION",
                        validation_status,
                        "Corrected query execution",
                    ),
                ]

                for column, metric in zip(
                    pg_cols,
                    pg_metrics,
                ):

                    label, value, meta = metric

                    with column:

                        render_html(
                            f"""
                            <div class="result-metric">
                                <div class="result-metric-label">
                                    {esc(label)}
                                </div>
                                <div class="result-metric-value">
                                    {esc(value)}
                                </div>
                                <div class="result-metric-meta">
                                    {esc(meta)}
                                </div>
                            </div>
                            """
                        )

                # ------------------------------------------------
                # Root cause
                # ------------------------------------------------

                missing_column = safe_text(
                    pg.get(
                        "column_name",
                        "Unknown column",
                    )
                )

                detected_table = safe_text(
                    pg.get(
                        "table_name",
                        "Unknown table",
                    )
                )

                column_matches = pg_column_search.get(
                    "matches",
                    []
                )

                render_html(
                    f"""
                    <div class="answer-card">
                        <div class="answer-label">
                            ROOT CAUSE DETECTED
                        </div>
                        <div class="answer-text">
                            Column <strong>{esc(missing_column)}</strong>
                            does not exist in
                            <strong>{esc(detected_table)}</strong>.
                        </div>
                    </div>
                    """
                )

                # ------------------------------------------------
                # Schema
                # ------------------------------------------------

                render_html(
                    """
                    <div class="code-result-title">
                        DATABASE SCHEMA
                    </div>
                    """
                )

                schema_columns = pg_schema.get(
                    "columns",
                    []
                )

                if schema_columns:

                    schema_rows = []

                    for item in schema_columns:

                        schema_rows.append(
                            {
                                "Column": item.get(
                                    "name",
                                    "Unknown",
                                ),
                                "Data Type": item.get(
                                    "data_type",
                                    "Unknown",
                                ),
                            }
                        )

                    st.dataframe(
                        schema_rows,
                        width="stretch",
                        hide_index=True,
                    )

                else:

                    st.info(
                        "No schema columns were returned."
                    )

                # ------------------------------------------------
                # Missing column discovery
                # ------------------------------------------------

                render_html(
                    """
                    <div class="code-result-title">
                        COLUMN DISCOVERY
                    </div>
                    """
                )

                if column_matches:

                    discovery_rows = [
                        {
                            "Table": match.get(
                                "table",
                                "Unknown",
                            ),
                            "Column": match.get(
                                "column",
                                "Unknown",
                            ),
                            "Data Type": match.get(
                                "data_type",
                                "Unknown",
                            ),
                        }
                        for match in column_matches
                    ]

                    st.dataframe(
                        discovery_rows,
                        width="stretch",
                        hide_index=True,
                    )

                else:

                    st.warning(
                        "The missing column was not found "
                        "in the inspected database schema."
                    )

                # ------------------------------------------------
                # JOIN analysis
                # ------------------------------------------------

                render_html(
                    """
                    <div class="code-result-title">
                        JOIN ANALYSIS
                    </div>
                    """
                )

                suggestions = pg_join.get(
                    "suggestions",
                    []
                )

                if suggestions:

                    for index, suggestion in enumerate(
                        suggestions,
                        start=1,
                    ):

                        render_html(
                            f"""
                            <div class="answer-card">
                                <div class="answer-label">
                                    JOIN OPTION {index}
                                </div>
                                <div class="answer-text">
                                    <strong>
                                        {esc(suggestion.get("source_table"))}
                                    </strong>
                                    →
                                    <strong>
                                        {esc(suggestion.get("target_table"))}
                                    </strong>
                                    using
                                    <strong>
                                        {esc(suggestion.get("join_column"))}
                                    </strong>
                                </div>
                            </div>
                            """
                        )

                else:

                    st.warning(
                        "No JOIN relationship could be inferred."
                    )

                # ------------------------------------------------
                # Corrected SQL
                # ------------------------------------------------

                render_html(
                    """
                    <div class="code-result-title">
                        CORRECTED SQL
                    </div>
                    """
                )

                if pg_corrected_sql:

                    st.code(
                        pg_corrected_sql,
                        language="sql",
                    )

                else:

                    st.info(
                        "No corrected SQL was generated."
                    )

                # ------------------------------------------------
                # Validation result
                # ------------------------------------------------

                if pg_validation:

                    if pg_validation.get("success"):

                        rows_returned = pg_validation.get(
                            "rows_returned",
                            0,
                        )

                        render_html(
                            f"""
                            <div class="verification-banner pass">
                                <div class="verification-icon">
                                    ✓
                                </div>
                                <div>
                                    <div class="verification-title">
                                        SQL Validation Passed
                                    </div>
                                    <div class="verification-text">
                                        The corrected SQL executed
                                        successfully and returned
                                        {esc(rows_returned)} sample rows.
                                    </div>
                                </div>
                            </div>
                            """
                        )

                        sample_rows = pg_validation.get(
                            "sample_rows",
                            []
                        )

                        if sample_rows:

                            st.dataframe(
                                sample_rows,
                                width="stretch",
                                hide_index=True,
                            )

                        else:

                            st.info(
                                "The corrected SQL is valid, but "
                                "the query returned 0 matching rows."
                            )

                    else:

                        render_html(
                            f"""
                            <div class="verification-banner fail">
                                <div class="verification-icon">
                                    !
                                </div>
                                <div>
                                    <div class="verification-title">
                                        SQL Validation Failed
                                    </div>
                                    <div class="verification-text">
                                        {esc(
                                            pg_validation.get(
                                                "error",
                                                "Unknown SQL validation error.",
                                            )
                                        )}
                                    </div>
                                </div>
                            </div>
                            """
                        )

                # ------------------------------------------------
                # Evidence
                # ------------------------------------------------

                render_html(
                    """
                    <div class="code-result-title">
                        DATABASE EVIDENCE
                    </div>
                    """
                )

                if isinstance(pg_evidence, list) and pg_evidence:

                    for index, evidence_item in enumerate(
                        pg_evidence,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}.** "
                            f"{safe_text(evidence_item)}"
                        )

                else:

                    st.info(
                        "No PostgreSQL evidence was returned."
                    )


    else:

        # ====================================================
        # EMPTY STATE
        # ====================================================

        render_html(
            """
            <div class="empty-card">

                <div class="empty-icon">
                    &lt;/&gt;
                </div>

                <div class="empty-title">
                    Ready to debug
                </div>

                <div class="empty-text">
                    Enter an error message and related code
                    above to start your debugging session.
                </div>

                <div class="empty-hints">

                    <span>PYTHON</span>
                    <span>SQL</span>
                    <span>POSTGRESQL</span>
                    <span>DOCKER</span>
                    <span>AIRFLOW</span>

                </div>

            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        <strong>DebugAI</strong>

        <span>•</span>

        Developer Debugging Platform

        <span>•</span>

        LangGraph · RAG · Specialized Tools

    </div>
    """
)
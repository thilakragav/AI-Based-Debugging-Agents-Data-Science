from agent.graph import build_debugging_graph


def run_test(name, error_message, code=""):
    print("\n")
    print("=" * 80)
    print(f"TEST: {name}")
    print("=" * 80)

    graph = build_debugging_graph()

    try:
        result = graph.invoke({
            "error_message": error_message,
            "code": code,
            "retry_count": 0
        })

        print("\nFINAL RESULT")
        print("-" * 80)

        print(
            result.get(
                "final_answer",
                "No final answer generated."
            )
        )

        print("\nROUTING INFORMATION")
        print("-" * 80)

        print(
            "Selected Agent:",
            result.get(
                "selected_agent",
                "Unknown"
            )
        )

        print(
            "Routing Reason:",
            result.get(
                "routing_reason",
                "Unknown"
            )
        )

        print(
            "Tool:",
            result.get(
                "tool_route",
                {}
            )
        )

        print("\nVERIFICATION")
        print("-" * 80)

        print(
            result.get(
                "verification",
                {}
            )
        )

    except Exception as e:

        print("\nERROR")
        print("-" * 80)

        print(type(e).__name__)
        print(str(e))


# ============================================================
# TEST 1 — PYTHON
# ============================================================

run_test(
    "PYTHON ERROR",

    """
    ModuleNotFoundError:
    No module named 'pandas'
    """,

    """
    import pandas as pd

    df = pd.read_csv("data.csv")
    print(df.head())
    """
)


# ============================================================
# TEST 2 — SQL
# ============================================================

run_test(
    "SQL ERROR",

    """
    SQL syntax error near FORM
    """,

    """
    SELECT *
    FORM customers;
    """
)


# ============================================================
# TEST 3 — POSTGRESQL
# ============================================================

run_test(
    "POSTGRESQL ERROR",

    """
    column "customer_name" does not exist
    """,

    """
    SELECT customer_name, order_id
    FROM orders;
    """
)


# ============================================================
# TEST 4 — DOCKER
# ============================================================

run_test(
    "DOCKER ERROR",

    """
    Cannot connect to the Docker daemon.
    Is the docker daemon running?
    """,

    """
    docker ps
    """
)


# ============================================================
# TEST 5 — AIRFLOW
# ============================================================

run_test(
    "AIRFLOW ERROR",

    """
    Broken DAG.
    Failed to import DAG.
    """,

    """
    from airflow import DAG

    dag = DAG("example")
    """
)
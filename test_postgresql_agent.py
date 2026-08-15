from agent.agents.postgresql_agent import (
    postgresql_agent
)


state = {

    "error_message":
        'column "customer_name" does not exist',

    "code":
        """
        SELECT customer_name, order_id
        FROM orders;
        """,

    "classification": {
        "technology": "postgresql",
        "category": "schema",
        "error_type": "UndefinedColumn"
    },

    "rag_context": """
    PostgreSQL Column Not Found

    Check the table, schema, column and aliases.
    Determine whether a JOIN is required.
    """
}


result = postgresql_agent(state)


print("=" * 60)
print("POSTGRESQL AGENT TEST")
print("=" * 60)

print(result["technology_analysis"])
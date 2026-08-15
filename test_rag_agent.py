from agent.agents.rag_agent import rag_agent


state = {

    "error_message":
        'column "customer_name" does not exist',

    "code":
        """
        SELECT customer_name, order_id
        FROM orders;
        """,

    "classification": {

        "technology":
            "postgresql",

        "category":
            "schema",

        "error_type":
            "UndefinedColumn"
    }
}


result = rag_agent(state)


print("=" * 60)
print("RAG AGENT TEST")
print("=" * 60)


print("\nRetrieved Documents:")

for document in result[
    "retrieved_documents"
]:

    print(
        "\nSource:",
        document["source"]
    )

    print(
        "Technology:",
        document["technology"]
    )

    print(
        "Category:",
        document["category"]
    )

    print(
        "Topic:",
        document["topic"]
    )


print("\n")
print("=" * 60)
print("RAG CONTEXT")
print("=" * 60)

print(
    result["rag_context"]
)
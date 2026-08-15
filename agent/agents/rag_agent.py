from rag.retriever import get_retriever


def rag_agent(state):
    """
    RAG Agent

    Retrieves knowledge relevant to the user's
    debugging problem based on technology.
    """

    error_message = state.get(
        "error_message",
        ""
    )

    code = state.get(
        "code",
        ""
    )

    classification = state.get(
        "classification",
        {}
    )

    technology = classification.get(
        "technology",
        ""
    )

    category = classification.get(
        "category",
        None
    )

    # --------------------------------------------------------
    # Build debugging query
    # --------------------------------------------------------

    query = f"""
    Debugging Problem

    Technology:
    {technology}

    Category:
    {category}

    Error:
    {error_message}

    Code:
    {code}
    """

    # --------------------------------------------------------
    # Get technology-specific retriever
    # --------------------------------------------------------

    retriever = get_retriever(
        technology=technology,
        category=category,
        k=4
    )

    # --------------------------------------------------------
    # Retrieve knowledge
    # --------------------------------------------------------

    documents = retriever.invoke(
        query
    )

    # --------------------------------------------------------
    # Build RAG context
    # --------------------------------------------------------

    rag_context = []

    retrieved_documents = []

    for document in documents:

        source = document.metadata.get(
            "source_file",
            "unknown"
        )

        retrieved_documents.append(
            {
                "source": source,
                "technology": document.metadata.get(
                    "technology"
                ),
                "category": document.metadata.get(
                    "category"
                ),
                "topic": document.metadata.get(
                    "topic"
                ),
                "content": document.page_content
            }
        )

        rag_context.append(
            f"""
SOURCE:
{source}

CONTENT:
{document.page_content}
"""
        )

    return {
        "rag_context": "\n\n".join(
            rag_context
        ),
        "retrieved_documents":
            retrieved_documents
    }
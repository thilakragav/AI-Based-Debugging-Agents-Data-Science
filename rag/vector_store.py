from pathlib import Path

from langchain_chroma import Chroma

from rag.embedding import get_embedding_model


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma_db"


# ---------------------------------------------------------
# Create Vector Store
# ---------------------------------------------------------

def create_vector_store(chunks):
    """
    Create a ChromaDB vector store from document chunks.
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    # Get Gemini embedding model
    embeddings = get_embedding_model()

    print(f"Creating ChromaDB with {len(chunks)} chunks...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="debugging_knowledge"
    )

    print("ChromaDB created successfully.")
    print(f"Database location: {CHROMA_DIR}")

    return vector_store
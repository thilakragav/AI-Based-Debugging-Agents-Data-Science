from pathlib import Path

from langchain_chroma import Chroma

from rag.embedding import get_embedding_model


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# GET VECTOR STORE
# ============================================================

def get_vector_store():

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name="debugging_knowledge",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    return vector_store


# ============================================================
# GET RETRIEVER
# ============================================================

def get_retriever(
    technology=None,
    category=None,
    k=4
):

    vector_store = get_vector_store()

    search_kwargs = {
        "k": k
    }

    # --------------------------------------------------------
    # Optional metadata filtering
    # --------------------------------------------------------

    if technology and category:

        search_kwargs["filter"] = {
            "$and": [
                {"technology": technology.lower()},
                {"category": category.lower()}
            ]
        }

    elif technology:

        search_kwargs["filter"] = {
            "technology": technology.lower()
        }

    elif category:

        search_kwargs["filter"] = {
            "category": category.lower()
        }

    # --------------------------------------------------------
    # Create retriever
    # --------------------------------------------------------

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )

    return retriever
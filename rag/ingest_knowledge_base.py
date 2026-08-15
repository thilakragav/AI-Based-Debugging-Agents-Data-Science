from pathlib import Path
import shutil

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from rag.embedding import get_embedding_model


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# CONFIGURATION
# ============================================================

COLLECTION_NAME = "debugging_knowledge"

CHUNK_SIZE = 800

CHUNK_OVERLAP = 100


# ============================================================
# EXTRACT METADATA
# ============================================================

def extract_metadata(file_path: Path):

    relative_path = file_path.relative_to(
        KNOWLEDGE_BASE_DIR
    )

    parts = relative_path.parts

    technology = parts[0] if len(parts) >= 1 else "unknown"

    category = parts[1] if len(parts) >= 2 else "general"

    topic = file_path.stem

    return {
        "technology": technology.lower(),
        "category": category.lower(),
        "topic": topic.lower(),
        "source_file": str(relative_path)
    }


# ============================================================
# LOAD MARKDOWN FILES
# ============================================================

def load_knowledge_base():

    documents = []

    markdown_files = list(
        KNOWLEDGE_BASE_DIR.rglob("*.md")
    )

    print(
        f"Found {len(markdown_files)} Markdown files."
    )

    for file_path in markdown_files:

        try:

            content = file_path.read_text(
                encoding="utf-8"
            )

            if not content.strip():
                continue

            metadata = extract_metadata(
                file_path
            )

            document = Document(
                page_content=content,
                metadata=metadata
            )

            documents.append(document)

        except Exception as e:

            print(
                f"Failed to load {file_path}: {e}"
            )

    return documents


# ============================================================
# SPLIT DOCUMENTS
# ============================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    return chunks


# ============================================================
# CREATE VECTOR STORE
# ============================================================

def create_vector_store(chunks):

    embeddings = get_embedding_model()

    # --------------------------------------------------------
    # Remove old database
    # --------------------------------------------------------

    if CHROMA_DIR.exists():

        print(
            "Removing existing Chroma database..."
        )

        shutil.rmtree(CHROMA_DIR)

    # --------------------------------------------------------
    # Create Chroma
    # --------------------------------------------------------

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR)
    )

    return vector_store


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DEBUGAI KNOWLEDGE BASE INGESTION")
    print("=" * 60)

    print(
        f"\nKnowledge Base:\n{KNOWLEDGE_BASE_DIR}"
    )

    print(
        f"\nChroma Database:\n{CHROMA_DIR}"
    )

    # --------------------------------------------------------
    # Check knowledge base
    # --------------------------------------------------------

    if not KNOWLEDGE_BASE_DIR.exists():

        raise FileNotFoundError(
            f"Knowledge base not found: "
            f"{KNOWLEDGE_BASE_DIR}"
        )

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    documents = load_knowledge_base()

    if not documents:

        raise ValueError(
            "No Markdown documents were found."
        )

    print(
        f"\nLoaded {len(documents)} documents."
    )

    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    chunks = split_documents(
        documents
    )

    # --------------------------------------------------------
    # Embed + Store
    # --------------------------------------------------------

    vector_store = create_vector_store(
        chunks
    )

    print("\nKnowledge base successfully indexed.")

    # --------------------------------------------------------
    # Count
    # --------------------------------------------------------

    try:

        count = vector_store._collection.count()

        print(
            f"Vectors stored in Chroma: {count}"
        )

    except Exception:

        pass

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
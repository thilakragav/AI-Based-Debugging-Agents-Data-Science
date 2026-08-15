from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


# ---------------------------------------------------------
# Load all PDFs
# ---------------------------------------------------------

def load_knowledge_base():
    """
    Load all PDF files from the knowledge_base directory.
    Add technology and source metadata to each document.
    """

    documents = []

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_BASE_DIR}"
        )

    pdf_files = list(KNOWLEDGE_BASE_DIR.rglob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found inside: {KNOWLEDGE_BASE_DIR}"
        )

    print(f"Found {len(pdf_files)} PDF files.\n")

    for pdf_path in pdf_files:

        # Folder name becomes the technology
        technology = pdf_path.parent.name.lower()

        print(f"Loading: {pdf_path.name}")
        print(f"Technology: {technology}")

        loader = PyMuPDFLoader(str(pdf_path))

        pdf_documents = loader.load()

        # Add metadata
        for document in pdf_documents:

            document.metadata.update({
                "technology": technology,
                "category": "debugging",
                "source": pdf_path.name
            })

        documents.extend(pdf_documents)

        print(f"Pages loaded: {len(pdf_documents)}")
        print("-" * 50)

    print(f"\nTotal pages loaded: {len(documents)}")

    return documents


# ---------------------------------------------------------
# Split documents into chunks
# ---------------------------------------------------------

def split_documents(documents):
    """
    Split loaded documents into smaller chunks.

    Metadata from the original documents is automatically
    preserved by LangChain.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Original documents/pages: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    return chunks


# ---------------------------------------------------------
# Test this file directly
# ---------------------------------------------------------

if __name__ == "__main__":

    documents = load_knowledge_base()

    chunks = split_documents(documents)

    print("\n========== SAMPLE CHUNK ==========\n")

    print(chunks[0].page_content[:1000])

    print("\n========== METADATA ==========\n")

    print(chunks[0].metadata)
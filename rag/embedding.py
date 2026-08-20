import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embedding_model():
    """
    Create and return the Google Gemini embedding model.

    The API key is loaded from the environment instead of
    being hardcoded in the source code.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )

    return embeddings
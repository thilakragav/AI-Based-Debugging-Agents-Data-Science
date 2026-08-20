import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# =========================================================
# ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    ENV_FILE,
    override=True
)


# =========================================================
# GROQ LLM
# =========================================================

def get_llm():

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY was not found. "
            "Check your .env file."
        )

    if not model:

        raise ValueError(
            "GROQ_MODEL was not found. "
            "Check your .env file."
        )

    return ChatGroq(
        model=model,
        groq_api_key=api_key,
        temperature=0
    )
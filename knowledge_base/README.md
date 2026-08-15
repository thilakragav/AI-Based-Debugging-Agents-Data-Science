# DebugAI Multi-Agent RAG Knowledge Base

This knowledge base is organized by technology and debugging topic.

## Technologies
- Python
- SQL
- PostgreSQL
- Docker
- Airflow

## RAG ingestion
Recommended metadata:
- technology
- category
- topic
- source_file

Example:
technology=postgresql
category=schema
topic=column_not_found

Load Markdown -> split into chunks -> embed -> store in the vector database -> retrieve using error + classification + code -> pass context to the RAG agent.

## Important
The documents provide debugging knowledge. Diagnostic tools should perform actual environment checks. Do not automatically execute destructive commands based only on retrieved text.

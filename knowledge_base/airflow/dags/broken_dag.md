# Airflow Broken DAG

## Meaning
Airflow cannot parse or import a DAG file.

## Common Checks
- Check Python syntax.
- Check imports.
- Check dependencies.
- Check project module availability.
- Inspect Airflow logs.

## Diagnostic / Example Commands
```bash
python -m py_compile dags/my_dag.py
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `broken_dag` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Airflow DAG Syntax Error

## Meaning
The DAG Python file contains invalid syntax.

## Common Checks
- Compile the DAG.
- Inspect the reported line and surrounding code.
- Re-run the parser after correction.

## Diagnostic / Example Commands
```bash
python -m py_compile dags/my_dag.py
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `dag_syntax_error` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Airflow PythonOperator

## Meaning
PythonOperator executes a Python callable as an Airflow task.

## Common Checks
- Check callable import.
- Check callable signature.
- Check dependencies.
- Inspect task logs.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `python_operator` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Airflow DAG Import Error

## Meaning
Airflow failed while importing a DAG module.

## Common Checks
- Check missing modules.
- Check PYTHONPATH/package layout.
- Check import-time code.
- Inspect scheduler/webserver logs.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `dag_import_error` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

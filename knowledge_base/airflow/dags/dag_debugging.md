# Airflow DAG Debugging

## Meaning
DAG debugging separates parsing/import problems from task execution problems.

## Common Checks
- Validate syntax.
- Validate imports.
- Check DAG configuration.
- Inspect Airflow logs.
- Verify DAG registration.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `dag_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

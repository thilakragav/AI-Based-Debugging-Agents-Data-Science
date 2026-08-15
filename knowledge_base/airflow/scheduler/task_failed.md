# Airflow Task Failed

## Meaning
A task entered a failed state because its underlying operation returned an error.

## Common Checks
- Read task logs.
- Identify the actual exception.
- Classify code/dependency/connection/data/infrastructure cause.
- Re-run after the fix.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `task_failed` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

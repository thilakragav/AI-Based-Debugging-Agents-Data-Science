# Airflow Scheduler Not Running

## Meaning
The scheduler is not processing DAG schedules as expected.

## Common Checks
- Check scheduler process/container.
- Inspect scheduler logs.
- Check metadata database connectivity.
- Check executor configuration.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `scheduler_not_running` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

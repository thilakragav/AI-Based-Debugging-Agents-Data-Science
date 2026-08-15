# Airflow Scheduler Debugging

## Meaning
Scheduler diagnosis uses scheduler logs, DAG parsing, database connectivity and task state transitions.

## Common Checks
- Check scheduler status.
- Check logs.
- Check DAG parsing.
- Check metadata database.
- Check task dependencies.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `scheduler_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

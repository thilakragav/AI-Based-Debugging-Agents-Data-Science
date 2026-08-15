# Airflow Operator Debugging

## Meaning
Operator debugging combines task logs, operator configuration, connections and the underlying operation.

## Common Checks
- Identify operator.
- Inspect logs.
- Validate parameters.
- Validate connection IDs.
- Reproduce the underlying command/query when practical.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `operator_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

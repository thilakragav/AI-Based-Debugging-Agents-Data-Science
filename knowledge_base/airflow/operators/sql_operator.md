# Airflow SQL Operator

## Meaning
A SQL operator executes SQL through a configured Airflow connection.

## Common Checks
- Validate SQL.
- Check connection ID.
- Check database connectivity.
- Check permissions and schema.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `sql_operator` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

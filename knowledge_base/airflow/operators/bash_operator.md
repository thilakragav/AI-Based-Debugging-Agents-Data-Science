# Airflow Bash Operator

## Meaning
A Bash-based operator runs a shell command inside the Airflow execution environment.

## Common Checks
- Check command availability.
- Check working directory.
- Check permissions.
- Check environment.
- Inspect non-zero exit codes.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `airflow` debugging and the `bash_operator` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

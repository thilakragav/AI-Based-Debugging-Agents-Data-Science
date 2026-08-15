# PostgreSQL Duplicate Key

## Meaning
An INSERT or UPDATE violates a primary-key or unique constraint.

## Common Checks
- Identify the violated constraint.
- Inspect the existing row.
- Check ingestion/upsert logic.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `duplicate_key` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

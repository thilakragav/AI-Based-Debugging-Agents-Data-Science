# PostgreSQL Common Errors

## Meaning
Common PostgreSQL failures include connection, authentication, schema, data-type and constraint errors.

## Common Checks
- Use the exact error message.
- Inspect database evidence.
- Inspect schema metadata.
- Verify the proposed fix against the database.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `postgres_common_errors` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

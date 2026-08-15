# PostgreSQL Undefined Table

## Meaning
PostgreSQL cannot resolve the referenced relation.

## Common Checks
- Check table name.
- Check schema.
- Check search path.
- Confirm the table was created.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `undefined_table` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# PostgreSQL Undefined Column

## Meaning
PostgreSQL cannot resolve a referenced column.

## Common Checks
- Check spelling.
- Check table alias.
- Check schema.
- Check whether the column belongs to another table.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `undefined_column` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# PostgreSQL Column Not Found

## Meaning
The referenced column does not exist in the referenced relation.

## Common Checks
- Check table.
- Check schema.
- Check column.
- Check aliases.
- Determine whether a JOIN is required.

## Diagnostic / Example Commands
```bash
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'orders';
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `column_not_found` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# PostgreSQL Table Not Found

## Meaning
PostgreSQL cannot resolve the referenced table/relation.

## Common Checks
- Check table spelling.
- Check schema.
- Check search_path.
- Use a schema-qualified name.

## Diagnostic / Example Commands
```bash
SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = 'orders';
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `table_not_found` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

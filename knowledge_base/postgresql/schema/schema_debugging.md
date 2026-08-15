# PostgreSQL Schema Debugging

## Meaning
Schema metadata provides evidence about tables, columns and data types.

## Common Checks
- Inspect schema.
- Inspect columns.
- Inspect data types.
- Inspect relationships.
- Use qualified names when needed.

## Diagnostic / Example Commands
```bash
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='orders';
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `schema_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

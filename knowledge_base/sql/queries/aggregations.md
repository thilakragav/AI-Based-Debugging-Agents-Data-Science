# SQL Aggregations

## Meaning
Aggregation functions summarize rows.

## Common Checks
- Validate GROUP BY columns.
- Check NULL handling.
- Compare aggregate results with a smaller dataset.

## Diagnostic / Example Commands
```bash
SELECT category, COUNT(*) FROM products GROUP BY category;
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `aggregations` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

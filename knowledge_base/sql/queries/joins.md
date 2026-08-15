# SQL Joins

## Meaning
Joins combine related rows from multiple tables.

## Common Checks
- Verify join keys.
- Choose the correct join type.
- Check for duplicate rows.
- Use explicit aliases.

## Diagnostic / Example Commands
```bash
SELECT o.order_id, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id;
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `joins` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# SQL Window Functions

## Meaning
Window functions calculate values across related rows without collapsing the result set.

## Common Checks
- Check PARTITION BY.
- Check ORDER BY.
- Validate ranking and running-total expectations.

## Diagnostic / Example Commands
```bash
SELECT customer_id, order_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) AS rn FROM orders;
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `window_functions` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

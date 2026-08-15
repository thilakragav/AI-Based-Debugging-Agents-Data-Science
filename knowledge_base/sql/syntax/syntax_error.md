# SQL Syntax Error

## Meaning
The SQL parser rejected the statement.

## Common Checks
- Check commas and parentheses.
- Check keywords and clause order.
- Check quoting.
- Reduce the query to a minimal failing statement.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `syntax_error` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

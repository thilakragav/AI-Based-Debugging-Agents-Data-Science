# SQL Subqueries

## Meaning
A subquery is a query nested inside another query.

## Common Checks
- Run the inner query independently.
- Check expected cardinality.
- Validate correlation conditions.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `subqueries` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

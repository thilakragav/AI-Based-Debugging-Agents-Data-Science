# SQL Query Debugging

## Meaning
A complex SQL query should be decomposed into independently verifiable parts.

## Common Checks
- Validate schema.
- Test base table.
- Test joins.
- Test filters.
- Test aggregation.
- Reassemble and verify.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `query_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

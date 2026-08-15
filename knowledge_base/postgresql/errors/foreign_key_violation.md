# PostgreSQL Foreign Key Violation

## Meaning
A child row references a missing parent key or a constrained parent row is being changed.

## Common Checks
- Check parent key.
- Check child key.
- Check operation order.
- Validate referential relationships.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `foreign_key_violation` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

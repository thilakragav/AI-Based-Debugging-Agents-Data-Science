# PostgreSQL Data Type Mismatch

## Meaning
An expression or assignment uses incompatible data types.

## Common Checks
- Inspect actual column types.
- Check parameters.
- Use explicit casts only when semantically correct.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `datatype_mismatch` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

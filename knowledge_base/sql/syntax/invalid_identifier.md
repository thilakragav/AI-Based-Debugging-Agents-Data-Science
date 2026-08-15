# SQL Invalid Identifier

## Meaning
A referenced table, column or alias cannot be resolved.

## Common Checks
- Verify table name.
- Verify column name.
- Verify aliases.
- Check quoting and case.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `invalid_identifier` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

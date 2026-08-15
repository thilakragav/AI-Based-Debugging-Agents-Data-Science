# SQL Invalid Syntax

## Meaning
The database cannot parse the submitted SQL.

## Common Checks
- Validate keywords.
- Validate parentheses.
- Validate expressions.
- Check database-specific syntax.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `invalid_syntax` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

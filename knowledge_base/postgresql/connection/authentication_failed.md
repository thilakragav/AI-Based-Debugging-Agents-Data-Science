# PostgreSQL Authentication Failed

## Meaning
The server was reached but rejected the supplied credentials or authentication configuration.

## Common Checks
- Verify username.
- Verify password securely.
- Verify database.
- Check authentication configuration.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `authentication_failed` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

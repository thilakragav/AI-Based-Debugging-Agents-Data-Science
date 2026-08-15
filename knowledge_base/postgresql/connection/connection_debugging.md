# PostgreSQL Connection Debugging

## Meaning
A PostgreSQL connection is defined by host, port, database, user and authentication settings.

## Common Checks
- Validate each connection parameter.
- Check server availability.
- Check authentication.
- Retry with a minimal client connection.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `connection_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# PostgreSQL Database Not Found

## Meaning
The server is reachable but the requested database cannot be opened.

## Common Checks
- Verify database name.
- Verify server endpoint.
- Check database availability and permissions.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `database_not_found` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

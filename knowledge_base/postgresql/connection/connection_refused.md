# PostgreSQL Connection Refused

## Meaning
The PostgreSQL client cannot establish a connection to the configured server endpoint.

## Common Checks
- Check server availability.
- Check host.
- Check port.
- Check container/service status.
- Check network access.

## Diagnostic / Example Commands
```bash
psql -h HOST -p PORT -U USER -d DATABASE
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `postgresql` debugging and the `connection_refused` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Docker Network Connection

## Meaning
Containers must share an appropriate network and use reachable service names/ports.

## Common Checks
- Inspect networks.
- Confirm container membership.
- Check service hostname.
- Check target port.

## Diagnostic / Example Commands
```bash
docker network ls
docker network inspect NETWORK
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `network_connection` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

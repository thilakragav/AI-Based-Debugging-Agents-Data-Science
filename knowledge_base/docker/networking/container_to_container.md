# Docker Container-to-Container Networking

## Meaning
Containers on a shared Docker network can communicate using service/container names when the application is listening correctly.

## Common Checks
- Check shared network.
- Use service name as hostname where appropriate.
- Verify target port.

## Diagnostic / Example Commands
```bash
docker network inspect NETWORK
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `container_to_container` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

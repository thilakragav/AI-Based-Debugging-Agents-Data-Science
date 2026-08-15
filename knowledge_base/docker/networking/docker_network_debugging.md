# Docker Network Debugging

## Meaning
Network diagnosis requires evidence from Docker network configuration and container status.

## Common Checks
- List networks.
- Inspect network.
- Confirm membership.
- Confirm hostname and port.
- Inspect service logs.

## Diagnostic / Example Commands
```bash
docker network ls
docker network inspect NETWORK
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `docker_network_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

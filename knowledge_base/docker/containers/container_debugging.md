# Docker Container Debugging

## Meaning
Container debugging combines status, logs, configuration, environment, ports and networks.

## Common Checks
- List containers.
- Inspect logs.
- Inspect configuration.
- Check environment and ports.
- Check networks.

## Diagnostic / Example Commands
```bash
docker ps -a
docker inspect CONTAINER
docker logs CONTAINER
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `container_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

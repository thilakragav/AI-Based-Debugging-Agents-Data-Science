# Docker Container Not Running

## Meaning
A container exists but is stopped or has exited.

## Common Checks
- List all containers.
- Inspect status.
- Read logs.
- Inspect configuration.
- Fix the underlying issue before repeated restarts.

## Diagnostic / Example Commands
```bash
docker ps -a
docker logs CONTAINER
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `container_not_running` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Docker Daemon Not Running

## Meaning
The Docker CLI cannot communicate with the Docker engine.

## Common Checks
- Check Docker installation.
- Check Docker context.
- Start Docker Desktop on Windows.
- Run docker info.

## Diagnostic / Example Commands
```bash
docker --version
docker context ls
docker info
docker ps
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `daemon_not_running` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Docker Installation Debugging

## Meaning
Docker CLI installation and Docker engine availability are separate checks.

## Common Checks
- Check docker executable.
- Check version.
- Check Docker Desktop on Windows.
- Check daemon connectivity.

## Diagnostic / Example Commands
```bash
docker --version
where docker
docker info
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `docker_installation` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

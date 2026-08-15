# Docker Container Logs

## Meaning
Container logs provide runtime evidence about application startup and failures.

## Common Checks
- Read current logs.
- Follow logs when diagnosing a live process.
- Correlate timestamps with the failure.

## Diagnostic / Example Commands
```bash
docker logs CONTAINER
docker logs -f CONTAINER
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `container_logs` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

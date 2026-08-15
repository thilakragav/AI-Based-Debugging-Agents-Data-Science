# Docker Port Mapping

## Meaning
Published ports map host ports to container ports.

## Common Checks
- Inspect published ports.
- Confirm the application listens on the intended container port.
- Confirm the host port is reachable.

## Diagnostic / Example Commands
```bash
docker ps
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `port_mapping` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

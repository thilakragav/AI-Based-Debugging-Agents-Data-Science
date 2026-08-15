# Docker Context Debugging

## Meaning
Docker context determines which Docker endpoint the CLI uses.

## Common Checks
- List contexts.
- Check active context.
- Verify the selected engine.

## Diagnostic / Example Commands
```bash
docker context ls
docker context show
docker info
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `docker` debugging and the `docker_context` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

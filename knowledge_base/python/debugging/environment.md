# Python Environment Debugging

## Meaning
Environment problems occur when the application and dependencies are not running under the expected interpreter.

## Common Checks
- Check Python version.
- Check executable path.
- Check pip path.
- Compare runtime environment with development environment.

## Diagnostic / Example Commands
```bash
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `environment` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

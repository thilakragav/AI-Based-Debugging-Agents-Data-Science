# Python Dependency Debugging

## Meaning
Dependency failures are usually caused by missing, incompatible or incorrectly installed packages.

## Common Checks
- Identify the failing import.
- Check installed version.
- Check requirements.
- Reinstall or pin a compatible version.
- Repeat the failing test.

## Diagnostic / Example Commands
```bash
python -m pip list
python -m pip freeze
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `dependency_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Python Virtual Environment

## Meaning
A virtual environment isolates project dependencies.

## Common Checks
- Create a project environment.
- Activate the correct environment.
- Verify the interpreter path.
- Install dependencies through that interpreter.

## Diagnostic / Example Commands
```bash
python -m venv venv
python -c "import sys; print(sys.executable)"
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `virtual_environment` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

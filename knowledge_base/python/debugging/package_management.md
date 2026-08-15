# Python Package Management

## Meaning
Packages should be installed and inspected through the Python interpreter used by the project.

## Common Checks
- Use python -m pip.
- Inspect installed versions.
- Maintain requirements.txt.

## Diagnostic / Example Commands
```bash
python -m pip list
python -m pip show PACKAGE
python -m pip install PACKAGE
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `package_management` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

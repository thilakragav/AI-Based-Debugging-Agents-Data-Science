# Python ModuleNotFoundError

## Meaning
Python cannot locate an imported module in the active environment.

## Common Checks
- Check the Python interpreter.
- Check whether the package is installed.
- Check the import name.
- Check the active virtual environment.

## Diagnostic / Example Commands
```bash
python --version
python -m pip show PACKAGE
python -c "import PACKAGE; print('Import successful')"
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `module_not_found` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# Python ImportError

## Meaning
Python found a module but could not import the requested name.

## Common Checks
- Verify the imported symbol exists.
- Check for circular imports.
- Check package version compatibility.
- Check whether a local file shadows the package.

## Diagnostic / Example Commands
```bash
python -c "import MODULE; print(MODULE)"
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `import_error` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

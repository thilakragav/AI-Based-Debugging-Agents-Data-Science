# Python TypeError

## Meaning
An operation or callable received an incompatible type or arguments.

## Common Checks
- Inspect runtime types.
- Check function arguments.
- Check whether an object is callable.

## Diagnostic / Example Commands
```bash
python -c "print(type(value))"
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `type_error` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

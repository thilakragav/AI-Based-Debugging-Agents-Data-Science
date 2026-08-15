# Python SyntaxError

## Meaning
Python cannot parse the source because its syntax is invalid.

## Common Checks
- Check brackets, commas, colons and indentation.
- Inspect the reported line and nearby lines.

## Diagnostic / Example Commands
```bash
python -m py_compile FILE.py
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `syntax_error` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

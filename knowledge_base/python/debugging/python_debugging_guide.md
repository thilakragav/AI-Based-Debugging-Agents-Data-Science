# Python Debugging Guide

## Meaning
A repeatable debugging process reduces guesswork.

## Common Checks
- Read the complete traceback.
- Identify exception type.
- Locate failing line.
- Inspect variables/types.
- Reproduce minimally.
- Fix and verify.

## Diagnostic / Example Commands
```bash
python -m py_compile FILE.py
```

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `python` debugging and the `python_debugging_guide` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

# SQL Debugging Guide

## Meaning
SQL debugging should isolate the failing clause and validate schema assumptions.

## Common Checks
- Check the exact database error.
- Validate tables and columns.
- Test joins separately.
- Test filters and aggregation separately.
- Run the corrected query.

## Verification
Use the original failing operation or a minimal reproduction to confirm that the diagnosis and proposed fix are correct.

## RAG Guidance
This document is relevant to `sql` debugging and the `sql_debugging` topic. Retrieve it when the user's error, classification, code, or tool evidence matches this topic.

## Safety
Prefer inspection and validation before changing production systems, deleting data, exposing credentials, or executing destructive commands.

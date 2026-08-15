from agent.tools import execute_python_debugging


print("=" * 70)
print("PYTHON DEBUGGING AGENT TEST")
print("=" * 70)


# =========================================================
# TEST ERROR
# =========================================================

error_message = """
ModuleNotFoundError: No module named 'pandas'
"""


# =========================================================
# CLASSIFICATION
# =========================================================

classification = {
    "technology": "python",
    "error_type": "ModuleNotFoundError",
    "category": "import"
}


print("\nERROR:")
print(error_message)

print("\nCLASSIFICATION:")
print(classification)


# =========================================================
# EXECUTE PYTHON DEBUGGING TOOL
# =========================================================

print("\n" + "=" * 70)
print("EXECUTING PYTHON DEBUGGING TOOL")
print("=" * 70)


result = execute_python_debugging(
    error_message=error_message,
    classification=classification
)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n" + "=" * 70)
print("PYTHON DEBUGGING RESULT")
print("=" * 70)

print(result)


# =========================================================
# DISPLAY IMPORTANT EVIDENCE
# =========================================================

print("\n" + "=" * 70)
print("IMPORTANT EVIDENCE")
print("=" * 70)


print("\nTechnology:")
print(result.get("technology"))


print("\nTool Executed:")
print(result.get("tool_executed"))


if "environment" in result:

    print("\nPython Environment:")
    print(result["environment"])


if "package" in result:

    print("\nPackage Information:")
    print(result["package"])


if "import" in result:

    print("\nImport Information:")
    print(result["import"])


print("\n" + "=" * 70)
print("TEST COMPLETED")
print("=" * 70)
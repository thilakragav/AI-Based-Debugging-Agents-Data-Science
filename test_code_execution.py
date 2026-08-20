from debugging.code_execution import execute_python_code


print("=" * 60)
print("CODE EXECUTION TEST")
print("=" * 60)


# =========================================================
# TEST 1 — SHOULD PASS
# =========================================================

print("\nTEST 1: Correct code")

code_pass = """
numbers = [1, 2, 3]
print(numbers[2])
"""

result = execute_python_code(code_pass)

print(result)


# =========================================================
# TEST 2 — SHOULD FAIL
# =========================================================

print("\nTEST 2: Incorrect code")

code_fail = """
numbers = [1, 2, 3]
print(numbers[10])
"""

result = execute_python_code(code_fail)

print(result)


# =========================================================
# TEST 3 — SHOULD BE BLOCKED
# =========================================================

print("\nTEST 3: Unsafe code")

code_blocked = """
import os
print(os.getcwd())
"""

result = execute_python_code(code_blocked)

print(result)
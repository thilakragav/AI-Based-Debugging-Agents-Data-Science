from debugging.error_classifier import classify_error


error = """
ERROR: column c.id does not exist
LINE 4: ON c.id = o.customer_id;
"""

result = classify_error(error)

print("=" * 60)
print("CLASSIFIER TEST")
print("=" * 60)
print(result)
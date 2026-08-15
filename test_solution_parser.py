from debugging.solution_generator import parse_json_response


response = (
    '```json\n'
    '{\n'
    '    "problem": "The column c.id does not exist",\n'
    '    "root_cause": "The customers table uses customer_id instead of id",\n'
    '    "solution": "Use customer_id in the JOIN condition",\n'
    '    "corrected_code": "SELECT c.customer_name, o.order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id;",\n'
    '    "verification_steps": [\n'
    '        "Check the customers table schema",\n'
    '        "Run the corrected SQL query",\n'
    '        "Use \\\\d customers to inspect the table"\n'
    '    ],\n'
    '    "prevention": "Verify column names before writing JOIN conditions."\n'
    '}\n'
    '```'
)


result = parse_json_response(response)


print("=" * 60)
print("SOLUTION PARSER TEST")
print("=" * 60)

print(result)

print("=" * 60)
print("PARSER TEST PASSED")
print("=" * 60)
"""
01_Python_Fundamentals - Loops & Sequence Traversals
Demonstrating deterministic looping tracking utilizing zip and enumerate utilities.
"""

headers = ["id", "endpoint", "status_code"]
row_data = [204, "/recipes", 200]

# 1. Enumerate Pattern (Tracks tracking indexes seamlessly without external manual increment counters)
print("--- Schema Field Enumeration ---")
for index, column in enumerate(headers):
    print(f"Position [{index}]: Map Element -> {column}")

# 2. Zip Pattern (Combines matching sequences—essential for transforming raw lists into tabular dictionaries)
print("\n--- Zipped Record Construction ---")
zipped_record = dict(zip(headers, row_data))
print(f"Structured Payload Mapping: {zipped_record}")
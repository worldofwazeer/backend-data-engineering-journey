"""
01_Python_Fundamentals - Conditionals & Truth Value Evaluations
Demonstrating clean branch gatekeepers, status routing, and pythonic None validations.
"""

api_response_status = 200
extracted_payload = None

# 1. Status Boundary Route Logic
if api_response_status == 200:
    print("Pipeline Execution: Success! Routing data streams to staging layers.")
elif api_response_status == 404:
    print("Pipeline Execution: Alert! Remote target endpoint not found.")
else:
    print(f"Pipeline Execution: Unhandled Exception Status Code [{api_response_status}]")

# 2. Explicit Identity Comparisons (The clean pythonic way to evaluate non-initialized states)
if extracted_payload is None:
    print("Data Integrity Check: Warning! Empty payload object identified.")
"""
01_Python_Fundamentals - Exception Handling
Demonstrating robust error containment architectures using target block capturing.
"""

raw_payload_data = {"id": 12, "metric": "invalid_numerical_string"}

try:
    print("Initiating volatile record conversion transformations...")
    # This will trigger a explicit ValueError since characters cannot be cast to base-10 integers
    converted_metric = int(raw_payload_data["metric"])

except KeyError as ke:
    print(f"Data Schema Failure: Target property field was absent in payload: {ke}")

except ValueError as ve:
    print(f"Data Transformation Failure: Data type casting violation captured: {ve}")

except Exception as general_error:
    print(f"Critical System Crash: Unmapped top-level error intercepted: {general_error}")

finally:
    print("Pipeline Execution Context Safety Sweep: System state cleared.")
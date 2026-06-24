"""
03_API_Requests - Status Code Verification
Demonstrating rigorous response verification gates using native raise mechanisms.
"""
import requests

TARGET_URL = "https://dummyjson.com/recipes"

response = requests.get(TARGET_URL, timeout=10)

# Explicitly handling response boundaries
if response.status_code == 200:
    print("Success: Endpoint reached and validation passed.")
else:
    print(f"Warning: Unexpected remote state encountered: {response.status_code}")

# The industry standard: Raise an exception automatically for any 4xx or 5xx error
response.raise_for_status()
print("Pipeline Check: Response payload structure cleared for processing.")
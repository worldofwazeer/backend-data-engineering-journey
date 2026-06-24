"""
03_API_Requests - Timeout Protections
Enforcing strict timeout boundaries to prevent blocking worker threads indefinitely.
"""
import requests

# Simulating a reliable configuration endpoint
TARGET_URL = "https://dummyjson.com/recipes"

try:
    # Production Rule: Never make a request without an explicit timeout float (connect, read)
    print("Initiating network operation with a strict 3.5-second threshold...")
    response = requests.get(TARGET_URL, timeout=3.5)
    print(f"Connection closed safely. Latency accepted. Status: {response.status_code}")

except requests.exceptions.Timeout:
    print("Critical Alert: Remote server exceeded connection latency threshold. Aborting pipeline step.")
"""
03_API_Requests - Hierarchical Error Containment
Implementing cascading catch traps for transport, routing, and remote outages.
"""
import requests

# Triggering an intentional 404 routing error
MALFORMED_URL = "https://dummyjson.com/invalid_endpoint_path"

try:
    response = requests.get(MALFORMED_URL, timeout=5)
    response.raise_for_status()

except requests.exceptions.HTTPError as http_err:
    print(f"Network Routing Error Caught (4xx/5xx): {http_err}")

except requests.exceptions.ConnectionError as conn_err:
    print(f"Infrastructure Transport Failure (DNS/Connection Refused): {conn_err}")

except requests.exceptions.Timeout as time_err:
    print(f"Latency Constraint Violated: {time_err}")

except requests.exceptions.RequestException as general_api_err:
    print(f"Top-level Ambiguous API Request Exception Intercepted: {general_api_err}")
"""
03_API_Requests - Query Parameter Management
Passing structured URL arguments cleanly using dictionary bindings.
"""
import requests

TARGET_URL = "https://dummyjson.com/recipes"

# Define parameters outside the string layout to let requests manage URL encoding securely
query_payload = {
    "limit": 5,
    "skip": 0,
    "select": "name,ingredients"
}

response = requests.get(TARGET_URL, params=query_payload, timeout=10)
response.raise_for_status()

data = response.json()
print(f"Paginated Extraction Success: Ingested {len(data.get('recipes', []))} limit records.")
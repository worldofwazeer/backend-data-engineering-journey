"""
03_API_Requests - Basic GET Request
Demonstrating clean initialization of HTTP client calls against remote endpoints.
"""
import requests

TARGET_URL = "https://dummyjson.com/recipes/1"

# In production, always initialize calls transparently
response = requests.get(TARGET_URL, timeout=10)

print(f"HTTP Connection Status Code: {response.status_code}")
print("Raw Text Snippet Extracted:")
print(response.text[:200])  # Print initial slice to verify stream connectivity
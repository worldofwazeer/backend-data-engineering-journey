"""
05_Data_Flattening - Flattening Users API Stream
Ingesting a real nested API data payload and extracting flat structures.
"""
import requests
from typing import List, Dict, Any

API_ENDPOINT = "https://dummyjson.com/users"

try:
    response = requests.get(API_ENDPOINT, params={"limit": 3}, timeout=10)
    response.raise_for_status()
    raw_data = response.json()

    flat_users_dim: List[Dict[str, Any]] = []

    for user in raw_data.get("users", []):
        # Extract and flatten elements out of complex nesting blocks
        flat_user = {
            "user_id": user.get("id"),
            "full_name": f"{user.get('firstName')} {user.get('lastName')}",
            "email": user.get("email"),
            "company_name": user.get("company", {}).get("name"),
            "company_department": user.get("company", {}).get("department"),
            "address_city": user.get("address", {}).get("city"),
            "address_coordinates_lat": user.get("address", {}).get("coordinates", {}).get("lat")
        }
        flat_users_dim.append(flat_user)

    print(f"Successfully processed and flattened {len(flat_users_dim)} user profiles.")
    print(f"Sample Row 1: {flat_users_dim[0]}")

except Exception as e:
    print(f"Pipeline Execution Aborted: {e}")
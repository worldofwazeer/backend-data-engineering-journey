"""
03_API_Requests - Production API Client Function
Bundling standard patterns into a reusable, type-hinted data engine component.
"""
from typing import Dict, Any, Optional
import requests


def fetch_production_api_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executes a guarded HTTP GET request against a targeted enterprise schema endpoint.

    :param endpoint: Targeted remote URL string.
    :param params: Optional key-value dictionary arguments for server filtering.
    :return: A parsed Python dictionary dataset.
    """
    try:
        # Combining timeout safeguards and query string controls
        response = requests.get(endpoint, params=params, timeout=7.0)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Pipeline Ingestion Interrupted at [{endpoint}]: Failure Context: {e}")
        # Return an empty schema structure to prevent downstream processing blocks from breaking
        return {"recipes": [], "total": 0, "error_state": True}


# Verification Execution
api_endpoint = "https://dummyjson.com/recipes"
filters = {"limit": 2}
clean_dataset = fetch_production_api_data(api_endpoint, params=filters)

print(f"Client Engine Execution Status: Verified {len(clean_dataset.get('recipes', []))} entries safely.")
"""
04_Nested_JSON - Safe Extraction Guards
Defensive parsing strategies to completely prevent KeyError crashes when fields are missing.
"""
from typing import Dict, Any

# A raw, imperfect real-world payload structure missing specific properties
corrupted_payload: Dict[str, Any] = {
    "client_id": "cli_102",
    "metrics": {
        "daily_requests": 1500
        # "monthly_total" is missing entirely from this stream block
    }
}

# The Safe Pattern: Chaining .get() fallback dictionary calls
daily = corrupted_payload.get("metrics", {}).get("daily_requests", 0)
monthly = corrupted_payload.get("metrics", {}).get("monthly_total", -1) # Defaults to -1 safely

print(f"Defensive Processing Output -> Daily: {daily} | Monthly (Fallback Applied): {monthly}")
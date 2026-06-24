"""
04_Nested_JSON - Nested Dictionaries
Demonstrating structural extraction from object-oriented dictionary maps.
"""
from typing import Dict, Any

# Simulated payload containing an internal configuration dictionary
enterprise_payload: Dict[str, Any] = {
    "company_name": "World_of_Wazeer Tech Ventures",
    "infrastructure": {
        "primary_db": "PostgreSQL",
        "port": 5432,
        "is_cloud": False
    }
}

# Accessing properties one level deep
db_type = enterprise_payload["infrastructure"]["primary_db"]
is_hosted = enterprise_payload["infrastructure"]["is_cloud"]

print(f"Ingestion Report: Source system runs on {db_type} (Cloud Hosted: {is_hosted})")
"""
04_Nested_JSON - Nested Lists
Iterating over sub-arrays embedded inside top-level parent keys.
"""
from typing import Dict, Any

# Simulated log with an array of objects
batch_payload: Dict[str, Any] = {
    "batch_id": 9942,
    "ingested_records": [
        {"id": 1, "status": "COMPLETED"},
        {"id": 2, "status": "FAILED"},
        {"id": 3, "status": "COMPLETED"}
    ]
}

print(f"Analyzing Batch ID: {batch_payload['batch_id']}")

# Unpacking the array loop sequence
for record in batch_payload["ingested_records"]:
    print(f" -> Record Reference: {record['id']} | Status Check: {record['status']}")
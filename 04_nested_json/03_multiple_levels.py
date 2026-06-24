"""
04_Nested_JSON - Deep Multi-Level Traversal
Drilling down through multiple tiers of nested schemas.
"""
from typing import Dict, Any

# Complex multi-layered API metadata payload
deep_json: Dict[str, Any] = {
    "status": "success",
    "data": {
        "pipeline": {
            "execution_meta": {
                "worker_node": "node_04",
                "allocated_cores": 8
            }
        }
    }
}

# Diving into tier 4 of the JSON object hierarchy
active_node = deep_json["data"]["pipeline"]["execution_meta"]["worker_node"]
assigned_cores = deep_json["data"]["pipeline"]["execution_meta"]["allocated_cores"]

print(f"Pipeline Topology System Check: Node = {active_node}, Cores = {assigned_cores}")
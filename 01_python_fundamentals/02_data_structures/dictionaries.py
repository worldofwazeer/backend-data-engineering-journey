"""
Dictionary manipulation, payload structuring, and safe dictionary merging.
Demonstrates TypedDict, dictionary view operations, and standard default handling.
"""
from collections import defaultdict
import logging
from typing import Any, TypedDict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# Define explicit schema shape for downstream pipeline consumption
class UserIngestRecord(TypedDict):
    user_id: int
    username: str
    email: str
    is_active: bool


def Merge_pipeline_configs(
    default_config: dict[str, Any], override_config: dict[str, Any]
) -> dict[str, Any]:
    """
    Merges configuration dictionaries using the union operator (|) available in Python 3.9+.
    Override keys take precedence.
    """
    return default_config | override_config


def aggregate_pipeline_metrics(raw_events: list[dict[str, Any]]) -> dict[str, list[int]]:
    """
    Aggregates metrics without KeyErrors using collections.defaultdict.
    """
    grouped_latencies: dict[str, list[int]] = defaultdict(list)

    for event in raw_events:
        service_name = event.get("service", "unknown_service")
        latency = event.get("latency_ms", 0)
        grouped_latencies[service_name].append(latency)

    return dict(grouped_latencies)


def manipulate_dict_views() -> None:
    """Demonstrates efficient dictionary view iterations (keys, values, items)."""
    payload: UserIngestRecord = {
        "user_id": 9942,
        "username": "ibrahim_wazeer",
        "email": "ibrahim@wazeer.tech",
        "is_active": True,
    }

    # Dict views reflect dynamic changes without re-copying keys into a list
    payload_keys = payload.keys()
    logging.info("Keys view before addition: %s", list(payload_keys))

    # Safe pop with fallback
    removed_email = payload.pop("email", None)
    logging.info("Extracted email: %s", removed_email)


if __name__ == "__main__":
    logging.info("--- Executing Dictionaries Module ---")

    # 1. Test dictionary merging (|)
    base_settings = {"timeout": 30, "retries": 3, "env": "development"}
    prod_overrides = {"env": "production", "retries": 5}
    final_config = Merge_pipeline_configs(base_settings, prod_overrides)

    assert final_config["env"] == "production"
    assert final_config["retries"] == 5
    assert final_config["timeout"] == 30
    logging.info("Config merge verified: %s", final_config)

    # 2. Test defaultdict aggregation
    events = [
        {"service": "auth_service", "latency_ms": 120},
        {"service": "etl_ingest", "latency_ms": 450},
        {"service": "auth_service", "latency_ms": 95},
    ]
    aggregated = aggregate_pipeline_metrics(events)
    assert len(aggregated["auth_service"]) == 2
    logging.info("Aggregated latencies: %s", aggregated)

    # 3. View manipulation
    manipulate_dict_views()
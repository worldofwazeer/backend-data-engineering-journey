"""
Advanced argument signatures and defensive parameter handling.
Demonstrates positional-only args (/), keyword-only args (*), and mutable default anti-pattern fixes.
"""
import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# 1. Positional-only (/) and Keyword-only (*) parameter enforcement
def configure_ingest_client(
    endpoint_url: str,
    /,  # Everything before '/' MUST be passed positionally
    *,  # Everything after '*' MUST be passed as keyword arguments
    timeout: float = 30.0,
    max_retries: int = 3,
    debug: bool = False,
) -> dict[str, Any]:
    """
    Demonstrates signature enforcement.
    Prevents positional errors on flags like 'debug' or 'timeout'.
    """
    return {
        "url": endpoint_url,
        "timeout": timeout,
        "retries": max_retries,
        "debug_mode": debug,
    }


# 2. Defensive Mutable Default Fix
def unsafe_append_log(message: str, log_history: list[str] = []) -> list[str]:
    """❌ ANTI-PATTERN: Shared mutable state across function calls."""
    log_history.append(message)
    return log_history


def safe_append_log(message: str, log_history: list[str] | None = None) -> list[str]:
    """
    ✅ PRODUCTION FIX: Default to None and instantiate a fresh container inside scope.
    """
    if log_history is None:
        log_history = []
    log_history.append(message)
    return log_history


# 3. Flexible Variable Arguments (*args, **kwargs)
def calculate_batch_metrics(*latencies: float, **metadata: Any) -> dict[str, Any]:
    """Demonstrates typed unpacking of arbitrary positional and keyword parameters."""
    if not latencies:
        avg_latency = 0.0
    else:
        avg_latency = sum(latencies) / len(latencies)

    return {
        "count": len(latencies),
        "avg_latency_ms": round(avg_latency, 2),
        "meta": metadata,
    }


if __name__ == "__main__":
    logging.info("--- Executing Arguments Module ---")

    # 1. Signature Test
    # configure_ingest_client("https://api.wazeer.tech", 10.0) -> Raises TypeError
    config = configure_ingest_client("https://api.wazeer.tech", timeout=10.0, debug=True)
    assert config["url"] == "https://api.wazeer.tech"
    assert config["timeout"] == 10.0

    # 2. Mutable Default Bug Proof vs Fix
    unsafe_1 = unsafe_append_log("Event A")
    unsafe_2 = unsafe_append_log("Event B")  # Reuses list from call 1!
    assert len(unsafe_2) == 2, "Unsafe function mutated shared state unexpectedly."

    safe_1 = safe_append_log("Event A")
    safe_2 = safe_append_log("Event B")
    assert len(safe_1) == 1 and len(safe_2) == 1, "Safe function preserved isolated state."
    logging.info("Mutable default fix verified.")

    # 3. Unpacking test
    metrics = calculate_batch_metrics(120.5, 98.2, 310.0, pipeline_id="pipe_99", status="OK")
    assert metrics["count"] == 3
    assert metrics["meta"]["pipeline_id"] == "pipe_99"
    logging.info("Batch metrics output: %s", metrics)
"""
Data structures and type management.
Focuses on choosing the right data type for the right scenario, emphasizing immutability and lookup efficiency.
"""
import sys
import logging
from typing import Mapping, Sequence, Set

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def demonstrate_scalars() -> None:
    """Demonstrates scalar (primitive) data types and memory allocation."""
    is_active: bool = True
    processed_rows: int = 1_500_000  # Syntactic sugar for readability
    latency_ms: float = 12.45

    logging.info(f"Integer Memory: {sys.getsizeof(processed_rows)} bytes")
    logging.info(f"Float Memory: {sys.getsizeof(latency_ms)} bytes")


def demonstrate_collections() -> None:
    """
    Demonstrates collection types, focusing on algorithmic complexity.
    - Lists: O(1) append, O(n) lookup.
    - Sets: O(1) lookup (hash map).
    - Tuples: Immutable, hashable, memory-efficient.
    - Dicts: Key-value mapping.
    """
    # 1. Tuple (Immutable - Safe for passing read-only coordinates or configs)
    db_coordinates: tuple[str, int] = ("postgres-prod-cluster.internal", 5432)

    # 2. Set (Unordered, Unique - Ideal for fast deduplication)
    seen_ids: Set[str] = {"tx_901", "tx_902", "tx_903"}
    seen_ids.add("tx_904")

    # 3. List (Mutable sequence - Ideal for ordered batch processing)
    # Using type aliases for clarity
    PayloadList = Sequence[dict[str, str]]
    failed_payloads: PayloadList = [
        {"id": "tx_905", "error": "timeout"},
        {"id": "tx_906", "error": "schema_mismatch"}
    ]

    # 4. Dictionary (Key-Value - Representing JSON/API responses)
    api_response: Mapping[str, any] = {
        "status": 200,
        "data": failed_payloads,
        "metadata": {"source": db_coordinates}
    }

    logging.info(f"Deduplicated IDs count: {len(seen_ids)}")
    logging.info(f"Extracted payload count: {len(api_response['data'])}")


if __name__ == "__main__":
    logging.info("--- Executing Data Types Module ---")
    demonstrate_scalars()
    demonstrate_collections()
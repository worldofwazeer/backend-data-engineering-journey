"""
Optimized sequence handling using Python lists.
Demonstrates batch chunking, list comprehensions, and memory-conscious operations for ETL pipelines.
"""
import logging
import sys
from typing import Any, Generator, Sequence

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def chunk_payload_batch(
    records: Sequence[dict[str, Any]], batch_size: int
) -> Generator[list[dict[str, Any]], None, None]:
    """
    Slices a large list into fixed-size mini-batches using list slicing.

    Memory Advantage: Uses a generator to yield chunks on demand
    rather than creating full in-memory duplicate copies.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")

    for i in range(0, len(records), batch_size):
        yield list(records[i : i + batch_size])


def process_list_transformations() -> None:
    """Demonstrates high-performance list operations and sorting."""
    raw_payloads = [
        {"event_id": "e_101", "latency": 120, "status": "SUCCESS"},
        {"event_id": "e_102", "latency": 450, "status": "FAILED"},
        {"event_id": "e_103", "latency": 85, "status": "SUCCESS"},
        {"event_id": "e_104", "latency": 310, "status": "FAILED"},
    ]

    # List comprehension for filtering and projecting fields cleanly
    high_latency_ids: list[str] = [
        item["event_id"]
        for item in raw_payloads
        if item["status"] == "FAILED" or item["latency"] > 200
    ]
    logging.info("High latency / failed event IDs: %s", high_latency_ids)

    # In-place sorting vs sorted()
    # list.sort() mutates in-place (O(n log n) Timsort), avoiding extra memory allocations
    raw_payloads.sort(key=lambda x: x["latency"], reverse=True)
    logging.info("Sorted by latency descending: First event is %s", raw_payloads[0]["event_id"])


def demonstrate_memory_growth() -> None:
    """Demonstrates how list over-allocation works under the hood in CPython."""
    dynamic_list: list[int] = []
    initial_size = sys.getsizeof(dynamic_list)

    # Observe memory jumps as CPython resizes the backing array
    sizes: list[int] = []
    for i in range(20):
        sizes.append(sys.getsizeof(dynamic_list))
        dynamic_list.append(i)

    logging.info("List memory allocation progression (bytes): %s", sizes[:8])


if __name__ == "__main__":
    logging.info("--- Executing Lists Module ---")

    # 1. Test batch generator
    mock_records = [{"id": i} for i in range(12)]
    batches = list(chunk_payload_batch(mock_records, batch_size=5))
    assert len(batches) == 3, "Should yield 3 batches (5, 5, 2)"
    logging.info("Batching assertion passed: Split 12 records into batch sizes %s", [len(b) for b in batches])

    # 2. Test transformations and memory
    process_list_transformations()
    demonstrate_memory_growth()
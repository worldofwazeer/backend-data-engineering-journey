"""
Structured return patterns and type-safe function outputs.
Demonstrates NamedTuples for multiple return values, explicit optionality, and early returns.
"""
import logging
from typing import NamedTuple, Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# Structured return type definition
class IngestionResult(NamedTuple):
    records_processed: int
    failed_count: int
    duration_seconds: float
    is_success: bool


def execute_batch_load(records: list[dict[str, any]]) -> IngestionResult:
    """
    Returns a strongly typed NamedTuple instead of an opaque raw tuple (a, b, c, d).
    Prevents positional unpacking bugs at caller sites.
    """
    if not records:
        return IngestionResult(
            records_processed=0,
            failed_count=0,
            duration_seconds=0.0,
            is_success=True,
        )

    failures = sum(1 for r in records if r.get("error"))
    processed = len(records) - failures

    return IngestionResult(
        records_processed=processed,
        failed_count=failures,
        duration_seconds=1.24,
        is_success=failures == 0,
    )


def find_first_corrupted_record(records: list[dict[str, any]]) -> Optional[dict[str, any]]:
    """
    Explicitly uses Optional to signify that None is a valid return outcome.
    Employs early return pattern for performance optimization.
    """
    for record in records:
        if "id" not in record or record.get("corrupted", False):
            return record  # Early exit on first match
    return None


if __name__ == "__main__":
    logging.info("--- Executing Return Values Module ---")

    payload = [
        {"id": "rec_01", "error": False},
        {"id": "rec_02", "error": True},
        {"id": "rec_03", "error": False},
    ]

    # Testing structured return
    result = execute_batch_load(payload)
    logging.info(
        "Batch Load Result -> Processed: %d, Failed: %d, Duration: %.2fs",
        result.records_processed,
        result.failed_count,
        result.duration_seconds,
    )
    assert result.records_processed == 2
    assert result.failed_count == 1
    assert result.is_success is False

    # Testing Optional early return
    corrupted = find_first_corrupted_record([{"id": "rec_10"}, {"corrupted": True}])
    assert corrupted is not None
    assert corrupted["corrupted"] is True
    logging.info("Found corrupted record via early return: %s", corrupted)
"""
First-class and higher-order function paradigms.
Demonstrates function passing, pipeline step composition, and type hinting Callable protocols.
"""
import logging
from typing import Callable, Any, Sequence

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Define type aliases for pipeline transformation functions
TransformFunc = Callable[[dict[str, Any]], dict[str, Any]]
FilterFunc = Callable[[dict[str, Any]], bool]


def clean_payload(record: dict[str, Any]) -> dict[str, Any]:
    """Transformation step: Standardizes key strings and strips whitespace."""
    cleaned = {}
    for key, val in record.items():
        clean_key = key.strip().lower()
        clean_val = val.strip() if isinstance(val, str) else val
        cleaned[clean_key] = clean_val
    return cleaned


def is_valid_user(record: dict[str, Any]) -> bool:
    """Filter step: Validates minimum schema requirement."""
    return bool(record.get("user_id") and record.get("status") == "active")


def execute_pipeline(
    records: Sequence[dict[str, Any]],
    transformers: Sequence[TransformFunc],
    filters: Sequence[FilterFunc],
) -> list[dict[str, Any]]:
    """
    Higher-order function that chains transformations and filters
    over a sequence of data payloads.
    """
    processed_records: list[dict[str, Any]] = []

    for raw_record in records:
        # Apply transformation steps sequentially
        current_record = raw_record
        for transform in transformers:
            current_record = transform(current_record)

        # Apply filter conditions
        if all(predicate(current_record) for predicate in filters):
            processed_records.append(current_record)

    return processed_records


if __name__ == "__main__":
    logging.info("--- Executing Functions Module ---")

    raw_data = [
        {" USER_ID ": "usr_101 ", "STATUS": " active ", "role": "admin"},
        {" USER_ID ": "usr_102 ", "STATUS": " pending ", "role": "guest"},
        {" USER_ID ": "", "STATUS": " active ", "role": "guest"},  # Invalid
    ]

    # Pipeline execution using composition
    output = execute_pipeline(
        records=raw_data,
        transformers=[clean_payload],
        filters=[is_valid_user],
    )

    assert len(output) == 1
    assert output[0]["user_id"] == "usr_101"
    assert output[0]["status"] == "active"
    logging.info("Higher-order function pipeline output: %s", output)
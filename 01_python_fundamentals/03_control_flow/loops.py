"""
Iteration patterns, bounded retry loops, and stream processing mechanics.
Highlights exponential backoff, for-else completion verification, and loop controls.
"""
import logging
import time
from typing import Sequence

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def execute_bounded_retry(max_retries: int = 3, initial_delay: float = 0.1) -> bool:
    """
    Demonstrates a bounded 'while' loop with exponential backoff logic.
    Prevents infinite loops when attempting transient remote operations.
    """
    attempt = 0
    delay = initial_delay

    while attempt < max_retries:
        attempt += 1
        logging.info("Attempt %d of %d executing...", attempt, max_retries)

        # Simulate network attempt (succeeds on 3rd attempt for demo)
        is_successful = attempt == 3

        if is_successful:
            logging.info("Operation succeeded on attempt %d", attempt)
            return True

        logging.warning("Attempt %d failed. Backing off for %.2fs...", attempt, delay)
        time.sleep(delay)
        delay *= 2  # Exponential backoff multiplier

    logging.error("Operation failed after exceeding max retries (%d)", max_retries)
    return False


def verify_batch_integrity(records: Sequence[dict[str, str]]) -> bool:
    """
    Demonstrates the Python 'for...else' construct.
    The 'else' block executes ONLY if the loop completes without encountering a 'break'.
    """
    for record in records:
        if "checksum" not in record or not record["checksum"]:
            logging.error("Corrupted record found ID: %s. Aborting batch execution.", record.get("id"))
            break  # Triggers exit; 'else' block will NOT execute
    else:
        # Reached only if loop finishes cleanly with no 'break'
        logging.info("All %d records validated successfully. Committing batch.", len(records))
        return True

    return False


def process_stream_with_skip(payloads: Sequence[dict[str, str]]) -> list[str]:
    """Demonstrates continue/break loop control mechanics during data processing."""
    processed_ids: list[str] = []

    for item in payloads:
        # Skip malformed items without stopping the loop
        if item.get("type") == "NOOP":
            continue

        # Immediate termination signal
        if item.get("type") == "POISON_PILL":
            logging.warning("Poison pill detected. Terminating stream execution early.")
            break

        processed_ids.append(item["id"])

    return processed_ids


if __name__ == "__main__":
    logging.info("--- Executing Loops Module ---")

    # 1. Bounded Retry Test
    retry_success = execute_bounded_retry(max_retries=3, initial_delay=0.01)
    assert retry_success is True, "Bounded retry should eventually succeed."

    # 2. For...Else Verification Test
    valid_batch = [
        {"id": "tx_1", "checksum": "a1b2"},
        {"id": "tx_2", "checksum": "c3d4"},
    ]
    invalid_batch = [
        {"id": "tx_1", "checksum": "a1b2"},
        {"id": "tx_3", "checksum": ""},  # Corrupted
    ]

    assert verify_batch_integrity(valid_batch) is True
    assert verify_batch_integrity(invalid_batch) is False

    # 3. Stream Control Test
    stream_data = [
        {"id": "evt_101", "type": "DATA"},
        {"id": "evt_102", "type": "NOOP"},
        {"id": "evt_103", "type": "DATA"},
        {"id": "evt_104", "type": "POISON_PILL"},
        {"id": "evt_105", "type": "DATA"},
    ]
    result = process_stream_with_skip(stream_data)
    assert result == ["evt_101", "evt_103"]
    logging.info("Stream processing controls verified successfully: Processed %s", result)
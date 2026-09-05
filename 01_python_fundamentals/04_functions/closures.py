"""
Stateful closures and function factories.
Demonstrates state encapsulation without classes, lightweight rate limiters, and counters.
"""
import logging
import time
from typing import Callable

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def create_rate_limiter(max_calls: int, time_window_sec: float) -> Callable[[], bool]:
    """
    Closure Factory: Encapsulates execution state inside an enclosed scope.
    Returns a rate-limiter function that tracks invocation timestamps.
    """
    call_timestamps: list[float] = []

    def allow_request() -> bool:
        nonlocal call_timestamps
        now = time.time()

        # Evict timestamps outside the sliding window
        call_timestamps = [ts for ts in call_timestamps if now - ts < time_window_sec]

        if len(call_timestamps) < max_calls:
            call_timestamps.append(now)
            return True

        return False

    return allow_request


def create_id_generator(prefix: str, start_id: int = 1000) -> Callable[[], str]:
    """
    Closure Factory: Creates an incrementing unique ID generator with a custom prefix.
    """
    current_id = start_id

    def generate_next_id() -> str:
        nonlocal current_id
        formatted_id = f"{prefix}_{current_id}"
        current_id += 1
        return formatted_id

    return generate_next_id


if __name__ == "__main__":
    logging.info("--- Executing Closures Module ---")

    # 1. Rate Limiter Closure Test
    # Allow 2 calls every 1.0 second
    rate_limiter = create_rate_limiter(max_calls=2, time_window_sec=1.0)

    assert rate_limiter() is True, "First request allowed"
    assert rate_limiter() is True, "Second request allowed"
    assert rate_limiter() is False, "Third request blocked by rate limiter"
    logging.info("Rate limiter closure successfully enforced sliding window quota.")

    # 2. ID Generator Closure Test
    tx_id_gen = create_id_generator(prefix="TX", start_id=500)

    assert tx_id_gen() == "TX_500"
    assert tx_id_gen() == "TX_501"
    assert tx_id_gen() == "TX_502"
    logging.info("Stateful closure generated sequential IDs cleanly.")
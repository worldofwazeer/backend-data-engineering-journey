"""
Advanced operator utilization.
Highlights identity vs equality, short-circuit evaluation, and bitwise flags.
"""
import logging
from typing import Optional, Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def demonstrate_identity_vs_equality() -> None:
    """
    A classic senior-level distinction.
    '==' checks if values are equivalent.
    'is' checks if they occupy the same exact memory address.
    """
    # Small integers are cached in Python (interning)
    a = 256
    b = 256
    assert a is b, "Small integers should be cached and share identity."

    # Lists are mutable, so they get distinct memory addresses even with identical contents
    list_a = [1, 2, 3]
    list_b = [1, 2, 3]

    assert list_a == list_b, "Values are equal."
    assert list_a is not list_b, "Memory addresses are different."
    logging.info("Identity vs Equality assertions passed.")


def demonstrate_short_circuit_evaluation(payload: Optional[dict[str, Any]] = None) -> None:
    """
    Uses 'and' / 'or' for safe evaluation without raising exceptions.
    Python stops evaluating as soon as the result is determined.
    """
    # Safe fallback using 'or'
    active_payload = payload or {"default": True, "items": []}

    # Safe extraction using 'and' to prevent KeyError or AttributeError
    # If active_payload is empty, it won't attempt to evaluate the second condition
    has_items = active_payload and len(active_payload.get("items", [])) > 0

    logging.info(f"Payload has items: {has_items}")


def demonstrate_membership_and_bitwise() -> None:
    """Demonstrates membership checks (in) and bitwise operations for flags."""
    # Membership (in) - O(1) lookup in sets
    allowed_methods = {"GET", "POST"}
    assert "GET" in allowed_methods, "GET should be allowed"

    # Bitwise operators (often used for permission flags or low-level parsing)
    READ = 0b0001
    WRITE = 0b0010
    EXECUTE = 0b0100

    user_permissions = READ | WRITE  # User has read and write (0b0011)

    # Check if user has write permission using bitwise AND (&)
    can_write = (user_permissions & WRITE) == WRITE
    logging.info(f"User has write permission: {can_write}")


if __name__ == "__main__":
    logging.info("--- Executing Operators Module ---")
    demonstrate_identity_vs_equality()
    demonstrate_short_circuit_evaluation(payload={"items": [1, 2, 3]})
    demonstrate_membership_and_bitwise()
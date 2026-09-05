"""
LEGB (Local, Enclosing, Global, Built-in) Scope Resolution.
Demonstrates scope hierarchies, local variable isolation, and 'nonlocal' mutation.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Global Scope Variable
GLOBAL_PIPELINE_ENV = "PRODUCTION"


def demonstrate_legb_resolution() -> dict[str, str]:
    """Demonstrates local shadowing without mutating the global scope."""
    # Local variable shadows global variable safely
    GLOBAL_PIPELINE_ENV = "STAGING_OVERRIDE"

    # Accessing built-in scope function: len()
    scope_info = {
        "local_env": GLOBAL_PIPELINE_ENV,
        "builtin_len_type": str(type(len)),
    }
    return scope_info


def demonstrate_nonlocal_mutation() -> tuple[int, int]:
    """
    Demonstrates mutating enclosing (outer) scope variables using 'nonlocal'.
    Essential for stateful function closures.
    """
    processed_counter = 0

    def increment_counter() -> None:
        nonlocal processed_counter  # Rebinds variable in enclosing function scope
        processed_counter += 1

    increment_counter()
    increment_counter()

    return processed_counter, 2


if __name__ == "__main__":
    logging.info("--- Executing Scope Module ---")

    # 1. LEGB Test
    local_info = demonstrate_legb_resolution()
    assert local_info["local_env"] == "STAGING_OVERRIDE"
    # Ensure outer global variable remained unchanged
    assert GLOBAL_PIPELINE_ENV == "PRODUCTION"
    logging.info("Global scope remained isolated: %s", GLOBAL_PIPELINE_ENV)

    # 2. Nonlocal Mutation Test
    count, expected = demonstrate_nonlocal_mutation()
    assert count == expected
    logging.info("Nonlocal counter successfully mutated enclosing scope state to: %d", count)
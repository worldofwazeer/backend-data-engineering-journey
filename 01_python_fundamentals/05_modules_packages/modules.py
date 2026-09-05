"""
Module Introspection and Execution Contexts.
Demonstrates how Python caches modules and handles execution contexts (script vs. import).
"""
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def inspect_module_state() -> dict[str, str]:
    """
    Demonstrates introspection of the current module's execution state.
    Understanding sys.modules and __name__ is a frequent requirement in technical
    architecture interviews for Python backend engineering.
    """
    return {
        "module_name": __name__,
        "module_file": __file__,
        "is_main_execution": str(__name__ == "__main__"),
        "is_cached_singleton": str(__name__ in sys.modules)
    }


def _verify_singleton_caching() -> None:
    """Shows that Python caches imported modules in sys.modules as singletons."""
    if __name__ in sys.modules:
        logging.info("Confirmed: Current module is cached in sys.modules.")


# The Execution Guard
# This block ONLY runs when the file is executed directly (e.g., `python modules.py`).
# It is completely ignored if the file is imported elsewhere (e.g., `import modules`).
if __name__ == "__main__":
    logging.info("--- Executing Modules Module Directly ---")

    state = inspect_module_state()
    logging.info("Module Introspection State:")
    for key, value in state.items():
        logging.info("  %s: %s", key, value)

    _verify_singleton_caching()
else:
    # This block executes if the file is imported by another script.
    # In production, avoid placing side-effects (like print statements) at the root level.
    logging.info("Module was imported as a dependency. (__name__ = %s)", __name__)
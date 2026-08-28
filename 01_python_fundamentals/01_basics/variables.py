
"""
Advanced variable management, scoping, and constant definitions.
Demonstrates type hinting, unpacking, and namespace hygiene suitable for pipeline configuration.
"""
import logging
from typing import Final, Any

# Configure basic logging for standard output
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# 1. Constants and Type Annotations
# Using Final prevents reassignment warnings in static type checkers (like mypy)
PIPELINE_NAME: Final[str] = "Customer_Data_Ingestion"
MAX_RETRIES: Final[int] = 5
CONNECTION_TIMEOUT_SEC: Final[float] = 30.5

# 2. Variable Unpacking (Destructuring)
def demonstrate_unpacking() -> None:
    """Demonstrates extracting values from data structures efficiently."""
    # Extracting head and tail from a simulated batch of record IDs
    record_ids = [101, 102, 103, 104, 105]
    first_record, *middle_records, last_record = record_ids

    logging.info(f"First ID: {first_record}, Last ID: {last_record}")
    logging.info(f"Middle batch size: {len(middle_records)}")

# 3. Scope and Namespace Management
def process_pipeline_config() -> dict[str, Any]:
    """Demonstrates local scoping shadowing global variables safely."""
    # Local variable masking a global concept cleanly within scope
    pipeline_state = "RUNNING"

    config = {
        "name": PIPELINE_NAME,
        "retries": MAX_RETRIES,
        "state": pipeline_state
    }
    return config

if __name__ == "__main__":
    logging.info("--- Executing Variables Module ---")
    demonstrate_unpacking()

    active_config = process_pipeline_config()
    logging.info(f"Active Configuration: {active_config}")
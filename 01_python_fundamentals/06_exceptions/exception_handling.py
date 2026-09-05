"""
The try / except / else / finally control flow.
Demonstrates proper resource cleanup and success-only execution paths.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def execute_database_transaction(payload: dict, force_failure: bool = False) -> None:
    """
    Demonstrates the complete exception handling matrix.
    Ensures a simulated database session is always closed, regardless of success or failure.
    """
    session_is_open = True
    logging.info("Session opened. Attempting transaction...")

    try:
        if force_failure:
            raise ValueError("Malformed payload detected during insert.")

        # Simulate processing
        record_id = payload.get("id")
        logging.info("Processing record: %s", record_id)

    except ValueError as e:
        # Executes ONLY if a ValueError is raised
        logging.error("Transaction rolled back due to error: %s", e)

    else:
        # Executes ONLY if the try block succeeds without exceptions
        logging.info("Transaction committed successfully.")

    finally:
        # Executes ALWAYS, whether an exception occurred or not.
        # This is where you release network connections, file handles, or driver instances (Playwright/Selenium).
        if session_is_open:
            session_is_open = False
            logging.info("Session closed and resources released.")


if __name__ == "__main__":
    logging.info("--- Executing Exception Handling Module ---")

    logging.info("\n--- Test 1: Successful Execution ---")
    execute_database_transaction({"id": "data_001"}, force_failure=False)

    logging.info("\n--- Test 2: Failed Execution ---")
    execute_database_transaction({"id": "data_002"}, force_failure=True)
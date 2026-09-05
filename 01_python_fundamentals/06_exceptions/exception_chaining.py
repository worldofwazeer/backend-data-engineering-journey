"""
Exception Chaining and Context Modification.
Demonstrates 'raise ... from ...' to wrap low-level errors into high-level domain errors.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class IngestionError(Exception):
    pass


def simulate_low_level_db_error():
    """Simulates a low-level library exception, like psycopg2.OperationalError."""
    raise ConnectionRefusedError("Connection refused by the server at 127.0.0.1:5432")


def run_pipeline_with_explicit_chaining():
    """
    ✅ GOOD: Explicit chaining.
    Wraps the low-level error in a domain error but preserves the original stack trace.
    """
    try:
        simulate_low_level_db_error()
    except ConnectionRefusedError as original_error:
        # The traceback will show: "The above exception was the direct cause of the following exception:"
        raise IngestionError("Pipeline extraction step failed") from original_error


def run_pipeline_suppressing_context():
    """
    Demonstrates suppressing the original exception context.
    Used when the underlying error contains sensitive information you do not want in the logs.
    """
    try:
        simulate_low_level_db_error()
    except ConnectionRefusedError:
        # The traceback will NOT show the original ConnectionRefusedError.
        raise IngestionError("A database error occurred. Details suppressed for security.") from None


if __name__ == "__main__":
    logging.info("--- Executing Exception Chaining Module ---")

    logging.info("\n1. Testing Explicit Chaining (raise from original)")
    try:
        run_pipeline_with_explicit_chaining()
    except IngestionError as e:
        logging.error("Caught error: %s", e)
        logging.error("Original cause was: %s", e.__cause__)

    logging.info("\n2. Testing Context Suppression (raise from None)")
    try:
        run_pipeline_suppressing_context()
    except IngestionError as e:
        logging.error("Caught error: %s", e)
        logging.error("Original cause was: %s (Successfully suppressed)", e.__cause__)
"""
06_Logging - Robust Exception Traceback Capture
Leveraging logger.exception() to automatically bind full stack traces inside error logs.
"""
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Boundary_Guard")

def parse_incoming_integer(raw_input: str) -> int:
    try:
        return int(raw_input)
    except ValueError:
        # Crucial Data Pattern: logger.exception automatically captures the entire crash traceback
        logger.exception(f"Fatal transformation error on data input reference: '{raw_input}'")
        raise

if __name__ == "__main__":
    try:
        parse_incoming_integer("malformed_payload_string")
    except ValueError:
        logger.error("Pipeline gracefully recovered. Moving corrupted payload to quarantine staging.")
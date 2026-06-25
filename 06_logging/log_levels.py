"""
06_Logging - Understanding Log Levels
Demonstrating log severity filtering to isolate development noise from production alerts.
"""
import logging

logging.basicConfig(
    level=logging.WARNING,  # Only log WARNING, ERROR, and CRITICAL to keep stdout clean
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # These two will NOT print because the active threshold level is set to WARNING
    logger.debug("Database raw query string generated: SELECT * FROM staging.users;")
    logger.info("API request completed successfully. Status code: 200")

    # These three WILL execute and output to stream
    logger.warning("Rate limit threshold approaching. 85% bandwidth consumed.")
    logger.error("Failed to parse row ID: 4042. Payload structural mapping error.")
    logger.critical("Database connection drop detected! Unable to reach master node.")
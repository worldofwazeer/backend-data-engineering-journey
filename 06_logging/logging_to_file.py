"""
06_Logging - Persistent File Logging
Directing automated ingestion audit streams directly to a physical log file.
"""
import logging
from pathlib import Path

# Ensure the logs directory exists structurally
log_directory = Path("06_logging/logs")
log_directory.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_directory / "ingestion_audit.log", mode="a"),
        logging.StreamHandler()  # Keeps output visible in PyCharm console as well
    ]
)

logger = logging.getLogger("DataLake_Ingestion_Engine")

if __name__ == "__main__":
    logger.info("Starting high-volume file transfer execution...")
    logger.info("Successfully mirrored 500 remote source objects to object storage.")
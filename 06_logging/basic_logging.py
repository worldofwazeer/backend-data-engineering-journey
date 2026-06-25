"""
06_Logging - Basic Logging Configuration
Setting up the standard stream handler to output structured logs to the console.
"""
import logging

# Configure the baseline logging format globally
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

def initialize_pipeline() -> None:
    logger.info("Initializing data ingestion framework components...")
    # Simulated pipeline setup steps
    logger.info("Connection pools established successfully.")

if __name__ == "__main__":
    initialize_pipeline()
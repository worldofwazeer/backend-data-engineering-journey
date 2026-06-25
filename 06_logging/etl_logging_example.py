"""
06_Logging - Production-Style ETL Audit Run
Putting all concepts together into a clean, type-hinted, audit-tracked pipeline simulation.
"""
import logging
from typing import List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger("ETL_Pipeline")


def extract_raw_records() -> List[Dict[str, Any]]:
    logger.info("ETL Phase 1/3: Extracting fresh transaction batch arrays from endpoint...")
    # Simulated batch data response
    return [
        {"item_id": 1, "price": 45.0},
        {"item_id": 2, "price": -10.0},  # Invalid data rule anomaly
        {"item_id": 3, "price": 120.5}
    ]


def transform_and_validate(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logger.info("ETL Phase 2/3: Launching structural validation transformation routines.")
    valid_records: List[Dict[str, Any]] = []

    for record in records:
        if record.get("price", 0) <= 0:
            logger.warning(f"Data anomaly filtered out -> Row ID {record.get('item_id')} has negative metric boundary.")
            continue
        valid_records.append(record)

    return valid_records


def load_to_warehouse(cleaned_data: List[Dict[str, Any]]) -> None:
    logger.info(f"ETL Phase 3/3: Committing {len(cleaned_data)} normalized records into destination warehouse tables.")
    logger.info("Transaction tracking sequence fully safe. Target synced.")


if __name__ == "__main__":
    logger.info("--- Starting Daily Automated Financial Data Pipeline ---")
    try:
        raw_stream = extract_raw_records()
        clean_stream = transform_and_validate(raw_stream)
        load_to_warehouse(clean_stream)
        logger.info("--- Data Ingestion Lifecycle Run Successfully [COMPLETED] ---")
    except Exception as e:
        logger.critical(f"Pipeline Ingestion crashed midway! Runtime error detail: {e}")
"""
Immutable sequence management with tuples and NamedTuples.
Emphasizes thread-safety, lower memory footprint, and returning structured data from pipeline stages.
"""
import sys
import logging
from typing import NamedTuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# 1. Standard Typed NamedTuple for structured pipeline metadata
class DatabaseConnectionConfig(NamedTuple):
    host: str
    port: int
    database: str
    ssl_enabled: bool = True

    def get_connection_url(self) -> str:
        """Helper method attached to immutable structure."""
        protocol = "postgresql+psycopg2" if self.ssl_enabled else "postgresql"
        return f"{protocol}://{self.host}:{self.port}/{self.database}"


def demonstrate_tuple_immutability() -> None:
    """Shows immutability benefits and memory comparison against lists."""
    # Tuples are stored in a single contiguous block of memory
    sample_list = ["postgres", 5432, "production_db", True]
    sample_tuple = ("postgres", 5432, "production_db", True)

    list_bytes = sys.getsizeof(sample_list)
    tuple_bytes = sys.getsizeof(sample_tuple)
    logging.info("Memory usage - List: %d bytes vs Tuple: %d bytes", list_bytes, tuple_bytes)

    # Tuples as composite keys in dictionaries (lists cannot be dict keys because they are unhashable)
    partition_offsets: dict[tuple[str, int], int] = {
        ("topic_analytics", 0): 104523,
        ("topic_analytics", 1): 104890,
    }

    current_offset = partition_offsets.get(("topic_analytics", 0))
    logging.info("Extracted offset for partition 0 using composite tuple key: %s", current_offset)


def parse_db_host(raw_url: str) -> tuple[str, int]:
    """Demonstrates returning multiple distinct typed elements securely via tuple unpacking."""
    parts = raw_url.replace("http://", "").replace("https://", "").split(":")
    host = parts[0]
    port = int(parts[1]) if len(parts) > 1 else 80
    return host, port  # Implicit tuple creation


if __name__ == "__main__":
    logging.info("--- Executing Tuples Module ---")

    # Execute NamedTuple functionality
    db_config = DatabaseConnectionConfig(
        host="db.internal.wazeer.tech",
        port=5432,
        database="ingestion_staging"
    )
    logging.info("Generated Connection URL: %s", db_config.get_connection_url())

    # Execute immutability and memory checks
    demonstrate_tuple_immutability()

    # Unpacking return values
    target_host, target_port = parse_db_host("db.internal.wazeer.tech:8080")
    assert target_host == "db.internal.wazeer.tech"
    assert target_port == 8080
    logging.info("Tuple unpacking verified successfully: Host=%s, Port=%d", target_host, target_port)
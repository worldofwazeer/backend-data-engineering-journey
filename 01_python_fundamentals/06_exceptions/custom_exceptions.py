"""
Domain-specific custom exception hierarchies.
Demonstrates defining business-logic errors for an ingestion pipeline
to differentiate between infrastructure, validation, and rate-limit failures.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class WazeerIngestionError(Exception):
    """
    Base exception for all data ingestion and pipeline errors.
    Allows upstream consumers to catch ANY pipeline error with a single block.
    """
    pass


class PostgresConnectionError(WazeerIngestionError):
    """Raised when the pipeline fails to connect to the PostgreSQL database."""

    def __init__(self, dsn: str, message: str = "Database connection failed"):
        self.dsn = dsn
        super().__init__(f"{message} (Target: {dsn})")


class ScrapingRateLimitError(WazeerIngestionError):
    """Raised when a target API or website enforces a rate limit (HTTP 429)."""

    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Must back off for {retry_after} seconds.")


class PayloadValidationError(WazeerIngestionError):
    """Raised when the scraped or ingested payload fails schema validation."""
    pass


if __name__ == "__main__":
    logging.info("--- Executing Custom Exceptions Module ---")

    # 1. Raising a rate limit error
    try:
        raise ScrapingRateLimitError(retry_after=60)
    except WazeerIngestionError as e:
        # We can catch the specific error using the base class
        logging.error("Pipeline interrupted by base ingestion error: %s", e)

    # 2. Raising a database error with custom attributes
    try:
        raise PostgresConnectionError(dsn="postgresql://user:pass@localhost:5432/dvdrental")
    except PostgresConnectionError as e:
        logging.error("Failed to connect. DSN attempting connection was: %s", e.dsn)
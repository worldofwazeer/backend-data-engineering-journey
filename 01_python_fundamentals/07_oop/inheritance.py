"""
Inheritance hierarchies and method overriding.
Demonstrates DRY principles and leveraging super() for extensible pipelines.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class BaseConnector:
    """Parent class defining universal connection logic."""

    def __init__(self, host: str):
        self.host = host
        self.connected = False

    def connect(self) -> None:
        self.connected = True
        logging.info("Base connector attached to %s", self.host)


class PostgresConnector(BaseConnector):
    """Child class inheriting from BaseConnector, specific to PostgreSQL."""

    def __init__(self, host: str, database: str):
        # Call the parent's __init__ to handle 'host'
        super().__init__(host)
        # Handle child-specific attributes
        self.database = database

    # Method Overriding
    def connect(self) -> None:
        """Overrides the parent method to inject PostgreSQL-specific logic."""
        super().connect()  # Optionally call the parent logic first
        logging.info("PostgreSQL dialect initialized for DB: %s", self.database)


if __name__ == "__main__":
    logging.info("--- Executing Inheritance Module ---")

    pg_client = PostgresConnector(host="localhost", database="dvdrental")
    pg_client.connect()

    assert pg_client.connected is True
    assert pg_client.host == "localhost"
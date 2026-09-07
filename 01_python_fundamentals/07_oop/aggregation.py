"""
Aggregation (Weak "Has-a" Relationship / Dependency Injection).
Demonstrates passing existing objects into other objects for loose coupling and testability.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class NetworkLogger:
    """Standalone component part."""

    def log(self, message: str) -> None:
        logging.info("[NETWORK] %s", message)


class APIClient:
    """
    Aggregate class.
    It receives an ALREADY CREATED logger from the outside.
    If the APIClient is destroyed, the NetworkLogger continues to exist independently.
    Highly preferred for scalable, testable systems (Dependency Injection).
    """

    def __init__(self, logger: NetworkLogger):
        self.logger = logger

    def fetch_data(self) -> None:
        self.logger.log("Fetching payloads via HTTP GET...")


if __name__ == "__main__":
    logging.info("--- Executing Aggregation Module ---")

    # The logger is created independently
    shared_logger = NetworkLogger()

    # Injected into the client
    client = APIClient(logger=shared_logger)
    client.fetch_data()

    # The client can be deleted, but the logger survives
    del client
    shared_logger.log("Client destroyed, but logger is still active.")
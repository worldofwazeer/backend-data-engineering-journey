"""
Composition (Strong "Has-a" Relationship).
Demonstrates objects owning other objects. If the parent dies, the child dies.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class QueryEngine:
    """Component part."""
    def execute(self, query: str) -> str:
        return f"Executed: {query}"


class DatabaseApplication:
    """
    Composite class.
    It creates the QueryEngine INSIDE its initializer.
    If the DatabaseApplication is destroyed, the QueryEngine is destroyed with it.
    """
    def __init__(self):
        # The engine is tightly coupled to the lifecycle of the application
        self.engine = QueryEngine()

    def run_job(self) -> None:
        result = self.engine.execute("SELECT * FROM users")
        logging.info("Database App result: %s", result)


if __name__ == "__main__":
    logging.info("--- Executing Composition Module ---")
    app = DatabaseApplication()
    app.run_job()
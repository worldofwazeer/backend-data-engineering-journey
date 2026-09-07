"""
Shared State and Attribute Shadowing.
Demonstrates the risks and use-cases of variables bound to the Class rather than the Instance.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class ConnectionPool:
    # Class Variable: Shared across ALL instances of ConnectionPool
    max_connections = 100

    def __init__(self, pool_name: str):
        # Instance Variable: Unique to THIS specific instance
        self.pool_name = pool_name


if __name__ == "__main__":
    logging.info("--- Executing Class Variables Module ---")

    pool_a = ConnectionPool("Analytics_DB")
    pool_b = ConnectionPool("Transactional_DB")

    # 1. Reading shared state
    assert pool_a.max_connections == 100
    assert pool_b.max_connections == 100

    # 2. Mutating the Class Variable (Affects everything)
    ConnectionPool.max_connections = 500
    logging.info("Mutated Class attribute. Pool A sees: %d, Pool B sees: %d",
                 pool_a.max_connections, pool_b.max_connections)

    # 3. Instance Shadowing (A common bug source)
    # This creates a NEW instance variable that masks/shadows the class variable for pool_a only
    pool_a.max_connections = 50

    assert pool_a.max_connections == 50  # Looks at shadowed instance var
    assert pool_b.max_connections == 500  # Still looks at shared class var
    logging.info("Pool A shadowed max_connections to 50. Pool B remains %d.", pool_b.max_connections)
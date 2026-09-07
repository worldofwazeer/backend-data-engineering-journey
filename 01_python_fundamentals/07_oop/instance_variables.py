"""
Instance State & Memory Optimization.
Demonstrates the standard `__dict__` state tracking and senior-level `__slots__` optimization.
"""
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class StandardRecord:
    """Uses a dynamic __dict__ for instance variables. Flexible but memory-heavy."""
    def __init__(self, record_id: int, payload: str):
        self.record_id = record_id
        self.payload = payload


class OptimizedRecord:
    """
    Uses __slots__ to pre-allocate memory space.
    Prevents the creation of __dict__, saving significant RAM when millions
    of these objects are loaded during data ingestion pipelines.
    """
    __slots__ = ['record_id', 'payload']

    def __init__(self, record_id: int, payload: str):
        self.record_id = record_id
        self.payload = payload


if __name__ == "__main__":
    logging.info("--- Executing Instance Variables Module ---")

    standard_obj = StandardRecord(1, "data")
    optimized_obj = OptimizedRecord(1, "data")

    # 1. Inspecting __dict__
    assert hasattr(standard_obj, "__dict__")
    assert not hasattr(optimized_obj, "__dict__")

    # 2. Memory Footprint Comparison
    # Note: sys.getsizeof() is superficial, but illustrates the base object overhead difference
    logging.info("Standard Object Size: %d bytes", sys.getsizeof(standard_obj))
    logging.info("Optimized (__slots__) Object Size: %d bytes", sys.getsizeof(optimized_obj))
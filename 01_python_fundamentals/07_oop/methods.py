"""
Method Types: Instance, Class (@classmethod), and Static (@staticmethod).
Demonstrates architectural design choices for method behavior and alternative constructors.
"""
import logging
from typing import Self

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class DataPayload:
    def __init__(self, raw_data: dict):
        self.raw_data = raw_data

    # 1. Instance Method (Requires 'self')
    def process(self) -> list:
        """Operates on the state of a specific instance."""
        return list(self.raw_data.values())

    # 2. Class Method (Requires 'cls' - usually used as alternative constructors)
    @classmethod
    def from_json_string(cls, json_str: str) -> Self:
        """
        Takes the Class itself as the first argument (cls).
        Used here as a factory method to instantiate the object from a different input type.
        """
        import json
        parsed_dict = json.loads(json_str)
        return cls(raw_data=parsed_dict)

    # 3. Static Method (Requires neither 'self' nor 'cls')
    @staticmethod
    def validate_schema(data: dict) -> bool:
        """
        A pure utility function logically grouped inside the class namespace.
        It cannot modify class or instance state.
        """
        return "id" in data


if __name__ == "__main__":
    logging.info("--- Executing Methods Module ---")

    # Testing Static Method (No instantiation required)
    is_valid = DataPayload.validate_schema({"id": 123})
    assert is_valid is True

    # Testing Class Method (Alternative Constructor)
    payload_obj = DataPayload.from_json_string('{"id": 99, "status": "active"}')
    assert isinstance(payload_obj, DataPayload)

    # Testing Instance Method
    values = payload_obj.process()
    logging.info("Processed values via instance method: %s", values)
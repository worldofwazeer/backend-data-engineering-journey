"""
01_Python_Fundamentals - Functions & Pure Transformations
Demonstrating clean decoupled components, strict type hinting, and documented returns.
"""

from typing import List, Dict, Any


def extract_high_value_records(records: List[Dict[str, Any]], price_threshold: float = 50.0) -> List[Dict[str, Any]]:
    """
    Parses a series of generic record payloads and filters targets above a financial threshold.

    :param records: List of dictionary records to process.
    :param price_threshold: Minimal criteria valuation float.
    :return: A filtered list of matches.
    """
    filtered_results = []
    for record in records:
        # Direct verification check
        if record.get("price", 0.0) >= price_threshold:
            filtered_results.append(record)

    return filtered_results


# Example execution with clean assertions
mock_stream = [{"id": 1, "price": 20.0}, {"id": 2, "price": 85.50}]
output = extract_high_value_records(mock_stream)
print(f"Processed Extraction Output: {output}")
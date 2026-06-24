"""
05_Data_Flattening - Flattening Nested Dictionaries
Demonstrating how to flatten a nested dictionary into a single-level tabular structure using pure Python.
"""
from typing import Dict, Any

# Raw semi-structured JSON payload
nested_profile: Dict[str, Any] = {
    "user_id": 1024,
    "username": "wazeer_ventures",
    "contact_info": {
        "email": "info@worldofwazeer.com",
        "location": {
            "state": "Gombe",
            "country": "Nigeria"
        }
    }
}


def flatten_dictionary(nested_dict: Dict[str, Any], parent_key: str = '', separator: str = '_') -> Dict[str, Any]:
    """
    Recursively flattens an infinitely nested dictionary mapping.
    """
    flat_items: Dict[str, Any] = {}

    for key, value in nested_dict.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            # Recursively flatten deeper levels
            flat_items.update(flatten_dictionary(value, new_key, separator=separator))
        else:
            flat_items[new_key] = value

    return flat_items


# Execute transformation
tabular_record = flatten_dictionary(nested_profile)
print("Transformation Complete. Tabular Record Struct:")
print(tabular_record)
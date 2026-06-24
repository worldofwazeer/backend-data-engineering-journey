"""
05_Data_Flattening - Flattening Lists of Primitive Objects
Demonstrating how to normalize array lists inside records into separate tabular entities.
"""
from typing import Dict, Any, List

# Record containing a nested array primitive
raw_product_record: Dict[str, Any] = {
    "product_id": 501,
    "title": "Wireless Mouse",
    "category_tags": ["Electronics", "Accessories", "Peripherals"]
}

# Goal: Flatten the 1-dimensional array into individual rows while preserving the parent context
flattened_rows: List[Dict[str, Any]] = []

for tag in raw_product_record["category_tags"]:
    flattened_rows.append({
        "product_id": raw_product_record["product_id"],
        "title": raw_product_record["title"],
        "assigned_tag": tag
    })

print(f"Generated {len(flattened_rows)} independent rows from nested primitive array:")
for row in flattened_rows:
    print(f" -> {row}")
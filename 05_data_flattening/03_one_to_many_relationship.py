"""
05_Data_Flattening - Relational Normalization (One-to-Many)
Splitting a nested payload into a distinct Parent table and Child table structure.
"""
from typing import Dict, Any, List

# Simulated order payload tracking items sold
order_payload: Dict[str, Any] = {
    "order_id": "TXN_99214",
    "customer_id": 4410,
    "order_total": 125.50,
    "line_items": [
        {"item_id": "ITM_01", "sku": "SSD-1TB", "price": 85.00},
        {"item_id": "ITM_02", "sku": "CABLE-USB", "price": 40.50}
    ]
}

# Table 1: Parent Order Details (Primary Key: order_id)
parent_order_row = {
    "order_id": order_payload["order_id"],
    "customer_id": order_payload["customer_id"],
    "order_total": order_payload["order_total"]
}

# Table 2: Child Line Items (Foreign Key: order_id)
child_items_rows: List[Dict[str, Any]] = []
for item in order_payload["line_items"]:
    child_items_rows.append({
        "order_id": order_payload["order_id"],  # Injected Foreign Key linkage
        "item_id": item["item_id"],
        "sku": item["sku"],
        "price": item["price"]
    })

print("Relational Database Schema Split:")
print(f" -> Parent Table Row: {parent_order_row}")
print(f" -> Child Table Rows Generated: {child_items_rows}")
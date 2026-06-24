"""
05_Data_Flattening - Flattening Carts Transaction Array
Extracting complex transactional line items directly from an API endpoint stream.
"""
import requests
from typing import List, Dict, Any

API_ENDPOINT = "https://dummyjson.com/carts"

try:
    response = requests.get(API_ENDPOINT, params={"limit": 2}, timeout=10)
    response.raise_for_status()
    raw_payload = response.json()

    flat_cart_items_fact: List[Dict[str, Any]] = []

    for cart in raw_payload.get("carts", []):
        cart_id = cart.get("id")
        user_id = cart.get("userId")

        # Unpacking nested product arrays inside individual carts
        for product in cart.get("products", []):
            flat_item_row = {
                "cart_id": cart_id,
                "user_id": user_id,
                "product_id": product.get("id"),
                "product_title": product.get("title"),
                "quantity": product.get("quantity"),
                "price_per_unit": product.get("price"),
                "row_total_price": product.get("total")
            }
            flat_cart_items_fact.append(flat_item_row)

    print(f"Flattening Success: Generated {len(flat_cart_items_fact)} transactional fact lines from Carts API.")
    print(f"Sample Transaction Row: {flat_cart_items_fact[0]}")

except Exception as e:
    print(f"Extraction Pipeline Stopped: {e}")
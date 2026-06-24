"""
05_Data_Flattening - Flattening Product Reviews Collection
Extracting a clean, relational staging structure from nested arrays inside product schemas.
"""
import requests
from typing import List, Dict, Any

API_ENDPOINT = "https://dummyjson.com/products"

try:
    response = requests.get(API_ENDPOINT, params={"limit": 2}, timeout=10)
    response.raise_for_status()
    products_payload = response.json()

    flat_reviews_table: List[Dict[str, Any]] = []

    for product in products_payload.get("products", []):
        product_id = product.get("id")
        product_sku = product.get("sku")

        # Isolating and looping through deep nested review objects
        for review in product.get("reviews", []):
            flat_review_row = {
                "product_id": product_id,
                "product_sku": product_sku,
                "reviewer_name": review.get("reviewerName"),
                "reviewer_email": review.get("reviewerEmail"),
                "rating_score": review.get("rating"),
                "comment_text": review.get("comment"),
                "created_at_timestamp": review.get("date")
            }
            flat_reviews_table.append(flat_review_row)

    print(f"Extraction Analytics Result: Flattened {len(flat_reviews_table)} total reviews from raw streams.")
    print(f"Sample Review Record: {flat_reviews_table[0]}")

except Exception as e:
    print(f"Analytics Staging Interrupted: {e}")
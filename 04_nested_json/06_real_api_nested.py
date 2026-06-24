"""
04_Nested_JSON - Real API Deep Extraction
Querying a real-world multi-tiered array endpoint and applying structural parsing rules.
"""
import requests

ENDPOINT_URL = "https://dummyjson.com/recipes"

try:
    # Querying a live slice array payload
    response = requests.get(ENDPOINT_URL, params={"limit": 1}, timeout=10)
    response.raise_for_status()
    payload = response.json()

    # Navigating: Root Dict -> 'recipes' List -> First Element Dict -> 'ingredients' List
    target_recipe = payload["recipes"][0]
    recipe_title = target_recipe["name"]
    nested_ingredients = target_recipe["ingredients"]

    print(f"Successfully Extracted Target: '{recipe_title}'")
    print(f"Parsing Nested Array Collection: Found {len(nested_ingredients)} nested ingredients items:")
    for item in nested_ingredients[:3]:  # Log a quick slice sample subset
        print(f" - {item}")

except Exception as err:
    print(f"Extraction Pipeline Stopped: {err}")
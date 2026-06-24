"""
03_API_Requests - JSON Payload Parsing
Safely transforming raw network stream text down into workable Python data structures.
"""
import requests

TARGET_URL = "https://dummyjson.com/recipes/1"

response = requests.get(TARGET_URL, timeout=10)
response.raise_for_status()

# Parsing the serialization wrapper into a native dictionary
recipe_dict = response.json()

print(f"Data Structure Cast Complete: Output target type is {type(recipe_dict)}")
print(f"Extracted Targeted Property -> Recipe Name: {recipe_dict.get('name')}")
print(f"Extracted Array Property -> Total Ingredients: {len(recipe_dict.get('ingredients', []))}")
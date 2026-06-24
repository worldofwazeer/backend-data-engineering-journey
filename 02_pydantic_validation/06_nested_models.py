"""
02_Pydantic_Validation - Nested Structural Models
Parsing complex hierarchical objects and child lists seamlessly.
"""
from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    quantity: str

class AdvancedRecipe(BaseModel):
    id: int
    recipe_name: str
    # Leveraging typing constructs to parse sub-arrays of objects
    ingredients: list[Ingredient]

hierarchical_json = {
    "id": 12,
    "recipe_name": "Matcha Tea",
    "ingredients": [
        {"name": "Matcha Powder", "quantity": "1 tsp"},
        {"name": "Hot Water", "quantity": "250ml"}
    ]
}

parsed_data = AdvancedRecipe(**hierarchical_json)
print(f"Successfully processed nested array containing {len(parsed_data.ingredients)} items.")
print(f"First Ingredient Name: {parsed_data.ingredients[0].name}")
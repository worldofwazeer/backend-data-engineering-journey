"""
02_Pydantic_Validation - Basic Model Ingestion
Demonstrating fundamental schema enforcement and strict type casting.
"""
from pydantic import BaseModel, ValidationError

class RecipePayload(BaseModel):
    id: int
    title: str
    servings: int

# Simulated raw payload (Notice 'id' is a string; Pydantic will auto-cast it safely)
raw_data = {"id": "105", "title": "Spaghetti Carbonara", "servings": 4}

try:
    recipe = RecipePayload(**raw_data)
    print(f"Schema Enforced Successfully: {recipe.title} (ID: {recipe.id})")
except ValidationError as e:
    print(f"Validation Failed:\n{e.json()}")
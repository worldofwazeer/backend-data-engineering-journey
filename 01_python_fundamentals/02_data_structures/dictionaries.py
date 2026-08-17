"""
01_Python_Fundamentals - Dictionaries Mastery
Demonstrating structured JSON representation, key access strategies, and mappings.
"""

# 1. Structured Data Layout (Simulating a single payload record)
recipe_payload = {
    "id": 1,
    "title": "Classic Lasagna",
    "prep_time_minutes": 30,
    "is_premium": False
}

# 2. Defensive Key Extraction (Using .get() to prevent unexpected KeyError crashes)
# If a key doesn't exist, it falls back to the default value gracefully
author = recipe_payload.get("author", "Anonymous Developer")
print(f"Recipe Contributor: {author}")

# 3. Dictionary Comprehension (Transforming key-value entries efficiently)
# Multiplying numerical parameters for metric conversions
scaled_payload = {k: (v * 2 if isinstance(v, int) else v) for k, v in recipe_payload.items()}
print(f"Scaled Processing Configuration: {scaled_payload}")
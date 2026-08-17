"""
01_Python_Fundamentals - Tuples Mastery
Demonstrating immutability use-cases and relational database row unpacking patterns.
"""

# 1. Immutable Infrastructure Configurations
# Tuples protect structural coordinates or settings from accidental runtime changes
DB_CONNECTION_POOL = ("127.0.0.1", 5432, "production_db")

# 2. Tuple Unpacking (Simulating reading a row returned from a database cursor)
db_row = (101, "Classic Lasagna", "Pasta")
recipe_id, recipe_name, category = db_row

print(f"Database Record Extracted:")
print(f" -> ID: {recipe_id}")
print(f" -> Target: {recipe_name}")
print(f" -> Category: {category}")
"""
01_Python_Fundamentals - Lists Mastery
Demonstrating sequence slicing, lists comprehensions, and data filtering patterns.
"""

# 1. Initialization & Modifying Sequences
ingested_topics = ["Python", "SQL", "Docker", "PostgreSQL"]
ingested_topics.append("Playwright")

# 2. Slicing (Essential for data batching & pagination concepts)
first_two_modules = ingested_topics[:2]
print(f"Initial Batch: {first_two_modules}")

# 3. List Comprehensions (The industry standard for clean data transformation)
# Standardizing text data to uppercase
clean_topics = [topic.upper() for topic in ingested_topics]
print(f"Normalized Topics: {clean_topics}")

# Inline filtering: Keep only items starting with 'P'
p_topics = [topic for topic in ingested_topics if topic.startswith("P")]
print(f"Filtered Ingestion Pipeline: {p_topics}")
# Challenge 2: Loop Architecture

**Given:**
You are pulling data from an API that has exactly 100 records. Your limit is 50.

**Questions:**
1. What does the API return when `skip=100`?
2. Why is it standard practice to use a `while True` loop instead of a fixed `for` loop (e.g., `for i in range(10)`) when building ingestion pipelines?
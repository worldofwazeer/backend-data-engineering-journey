# Authenticated API Ingestion Module

This module implements a production-grade, highly resilient HTTP client utilizing Python's object-oriented paradigms to handle authenticated API data ingestion defensively.

## 🚀 Core Features

- **Resource-Safe Context Management:** Implements `__enter__` and `__exit__` magic methods to wrap connection pooling in standard Python `with` blocks, eliminating socket and memory leaks.
- **Defensive Payload Validation:** Explicitly checks the `Content-Type` header (`"application/json" in content_type`) before invoking parsing methods to catch HTML maintenance pages served under standard `200 OK` statuses.
- **Intelligent Fault Tolerance:** Built-in exponential backoff retry loop that respects server constraints by dynamically extracting and honoring the `Retry-After` header on rate limits (`HTTP 429`).
- **Clean State Persistence:** Preserves exception contexts to guarantee clear stack traces upon pipeline failure instead of inducing raw runtime errors.
- **Decoupled Architecture:** Centralized runtime configurations (`.env`) isolated entirely from structural request logic.

## 📁 Directory Structure

```text
authentication/
├── api_client.py             # Reusable, validated HTTP client class
├── authenticated_pipeline.py # End-to-end pipeline execution runner
├── config.py                 # Centralized configuration mapping
├── .env.example              # Template for environment credentials
└── notes.md                  # Detailed architectural and engineering takeaways
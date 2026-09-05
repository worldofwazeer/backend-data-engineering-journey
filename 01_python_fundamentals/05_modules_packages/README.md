# Module 05: Modules, Packages & Import Architecture

This directory covers senior-level module management and import architecture in Python. It focuses on resolving circular dependencies, controlling public APIs, and understanding Python's module caching mechanics—key concepts for technical engineering interviews and resilient data ingestion frameworks.

## Core Concepts & Senior-Level Focus
* **The Execution Guard (`if __name__ == "__main__":`):** Isolating script execution logic from import behavior to prevent side-effects during testing or pipeline orchestration.
* **Public API Encapsulation (`__all__`):** Explicitly declaring which functions and classes are exposed when a consumer uses `from module import *`, hiding internal helper functions.
* **Lazy Loading:** Deferring heavy imports until runtime to speed up initial pipeline execution and gracefully resolve circular import errors.
* **Module Caching (`sys.modules`):** Understanding that Python modules act as singletons, evaluated only once upon first import and cached in memory.
* **Optional Dependencies:** Implementing safe fallback `try/except ImportError` blocks for pipelines that can run in degraded modes if certain third-party packages are missing.

## Module Execution
Execute each module directly to run built-in assertion tests and introspection outputs:
```bash
python imports.py
python modules.py
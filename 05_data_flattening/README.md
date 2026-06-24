# 05 - Data Flattening & Structural Normalization

## 🎯 Strategic Objective
This module implements production strategies to untangle hierarchical JSON structures and nested object lists into structured tables. This stage is necessary for populating relational target systems (PostgreSQL, BigQuery) without duplicating storage volumes unprofessionally.

## 🛠️ Concepts Demonstrated
* **Recursive Dictionary Parsing:** Dynamically traversing nested dictionaries to safely generate standardized snake_case column formats.
* **One-to-Many Relational Isolation:** Uncoupling transactional nested arrays from core object details to construct linked Parent/Child schemas.
* **Granular Array Extraction:** Extracting items from live endpoints (Carts, Products Reviews) and converting them into analytics-ready rows.
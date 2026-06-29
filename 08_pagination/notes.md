# Pagination & Pipeline Notes

* **limit**: The maximum number of records requested in a single API call.
* **skip** (or offset): The number of records to bypass before starting extraction.
* **while True**: Continues requesting pages indefinitely until explicitly broken.
* **Break condition**: `if not records: break` stops the loop when the API returns `[]`.
* **.extend()**: Used to flatten and combine multiple lists (pages) into a single master dataset.
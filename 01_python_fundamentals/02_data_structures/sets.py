"""
Set theory and high-performance deduplication.
Demonstrates O(1) membership testing, set algebra for database reconciliation, and frozenset usage.
"""
import logging
from typing import AbstractSet

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def reconcile_database_records(
        source_ids: set[str], target_ids: set[str]
) -> dict[str, set[str]]:
    """
    Uses set operations to determine missing, matched, and orphaned records
    between source and destination databases during an ETL sync.

    Set Algebra:
    - Difference (-): Items in left set but not right set.
    - Intersection (&): Items existing in both sets.
    - Symmetric Difference (^): Items in either set, but NOT both.
    """
    missing_in_target = source_ids - target_ids  # Source IDs that failed to ingest
    orphaned_in_target = target_ids - source_ids  # Target IDs deleted from source
    synchronized_records = source_ids & target_ids  # Fully reconciled records
    unmatched_discrepancies = source_ids ^ target_ids  # Total mismatch count

    return {
        "missing_in_target": missing_in_target,
        "orphaned_in_target": orphaned_in_target,
        "synchronized": synchronized_records,
        "total_discrepancies": unmatched_discrepancies,
    }


def demonstrate_frozenset() -> None:
    """
    Demonstrates immutable frozenset used for immutable lookup policies
    and dictionary keys.
    """
    # Standard sets are mutable and unhashable
    # frozenset is immutable and hashable
    IMMUTABLE_ALLOWED_ROLES: AbstractSet[str] = frozenset({"admin", "ingestion_engine", "read_only"})

    role_permissions: dict[frozenset[str], list[str]] = {
        frozenset({"admin", "ingestion_engine"}): ["SELECT", "INSERT", "UPDATE", "DELETE"],
        frozenset({"read_only"}): ["SELECT"],
    }

    logging.info("Frozenset lookup test: %s", role_permissions[IMMUTABLE_ALLOWED_ROLES - frozenset({"read_only"})])


if __name__ == "__main__":
    logging.info("--- Executing Sets Module ---")

    # Mock IDs from source DB vs target warehouse DB
    db_source_ids = {"usr_101", "usr_102", "usr_103", "usr_104", "usr_105"}
    dw_target_ids = {"usr_101", "usr_102", "usr_103", "usr_999"}

    reconciliation = reconcile_database_records(db_source_ids, dw_target_ids)

    assert reconciliation["missing_in_target"] == {"usr_104", "usr_105"}
    assert reconciliation["orphaned_in_target"] == {"usr_999"}
    assert reconciliation["synchronized"] == {"usr_101", "usr_102", "usr_103"}

    logging.info("Reconciliation results:")
    logging.info("  - Missing records to ingest: %s", reconciliation["missing_in_target"])
    logging.info("  - Orphaned warehouse records: %s", reconciliation["orphaned_in_target"])
    logging.info("  - Synchronized records count: %d", len(reconciliation["synchronized"]))

    demonstrate_frozenset()
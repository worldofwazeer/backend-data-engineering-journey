"""
Production conditional branching logic and pattern matching.
Demonstrates guard clauses, structural pattern matching (match-case), and ternary evaluation.
"""
import logging
from typing import Any, Mapping

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def evaluate_api_response_match(response: Mapping[str, Any]) -> str:
    """
    Demonstrates Structural Pattern Matching (match-case) introduced in Python 3.10.
    Parses incoming payload shapes and status codes declaratively.
    """
    match response:
        case {"status": 200, "data": [*items]} if len(items) > 0:
            return f"SUCCESS_WITH_DATA:{len(items)}_RECORDS"
        case {"status": 200, "data": []}:
            return "SUCCESS_EMPTY_PAYLOAD"
        case {"status": 429, "retry_after": int(seconds)}:
            return f"RATE_LIMITED_WAIT_{seconds}S"
        case {"status": status_code} if status_code >= 500:
            return f"SERVER_ERROR_{status_code}"
        case _:
            return "UNHANDLED_RESPONSE_SCHEMA"


def process_record_with_guards(record: Mapping[str, Any]) -> str:
    """
    Demonstrates the Guard Clause / Early Return pattern.
    Replaces deeply nested 'if-else' trees with flat, readable validation checks.
    """
    # Guard 1: Null check
    if not record:
        raise ValueError("Record payload cannot be empty.")

    # Guard 2: Schema validation
    if "id" not in record or "status" not in record:
        return "INVALID_SCHEMA"

    # Guard 3: Status check
    if record["status"] != "PENDING":
        return f"SKIPPED_STATUS_{record['status']}"

    # Main execution path (reached only when all guards pass, with zero nesting)
    record_id = record["id"]
    return f"PROCESSED_{record_id}"


def evaluate_feature_flag(env: str, custom_flag: bool | None = None) -> bool:
    """Demonstrates safe ternary expressions with fallback checks."""
    # Inline ternary evaluation with default fallbacks
    is_production = True if env.lower() == "production" else False
    return custom_flag if custom_flag is not None else not is_production


if __name__ == "__main__":
    logging.info("--- Executing Conditionals Module ---")

    # 1. Pattern Matching Tests
    resp_success = {"status": 200, "data": [{"id": 1}, {"id": 2}]}
    resp_rate_limit = {"status": 429, "retry_after": 60}

    assert evaluate_api_response_match(resp_success) == "SUCCESS_WITH_DATA:2_RECORDS"
    assert evaluate_api_response_match(resp_rate_limit) == "RATE_LIMITED_WAIT_60S"
    logging.info("Pattern matching assertions passed.")

    # 2. Guard Clause Tests
    assert process_record_with_guards({}) == "INVALID_SCHEMA"  # via key check guard
    assert process_record_with_guards({"id": "rec_001", "status": "COMPLETED"}) == "SKIPPED_STATUS_COMPLETED"
    assert process_record_with_guards({"id": "rec_002", "status": "PENDING"}) == "PROCESSED_rec_002"
    logging.info("Guard clause assertions passed.")

    # 3. Ternary Tests
    assert evaluate_feature_flag("production") is False
    assert evaluate_feature_flag("staging", custom_flag=True) is True
    logging.info("Ternary flag evaluation passed.")
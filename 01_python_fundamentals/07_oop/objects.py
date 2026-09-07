"""
Instantiation, Object Identity, and Memory Allocation.
Demonstrates that distinct objects possess unique memory addresses and isolated states.
"""
import logging
from classes import ExtractorBlueprint

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


if __name__ == "__main__":
    logging.info("--- Executing Objects Module ---")

    # Instantiating two distinct objects from the same class blueprint
    extractor_alpha = ExtractorBlueprint(target_url="https://api.wazeer.tech/v1", timeout=15)
    extractor_beta = ExtractorBlueprint(target_url="https://api.wazeer.tech/v2", timeout=45)

    # 1. State Isolation Verification
    assert extractor_alpha.timeout == 15
    assert extractor_beta.timeout == 45
    logging.info("State isolation verified: Alpha (%ds), Beta (%ds)",
                 extractor_alpha.timeout, extractor_beta.timeout)

    # 2. Identity and Memory Verification
    # 'is' checks if they point to the exact same memory address (identity)
    assert extractor_alpha is not extractor_beta
    logging.info("Memory isolation verified: Alpha ID: %s, Beta ID: %s",
                 id(extractor_alpha), id(extractor_beta))
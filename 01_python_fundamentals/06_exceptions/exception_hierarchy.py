"""
Exception Hierarchies and System Interrupts.
Demonstrates why we catch 'Exception' instead of 'BaseException' or using bare 'except:'.
"""
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def unsafe_bare_except():
    """
    ❌ ANTI-PATTERN: A bare 'except:' catches BaseException.
    This prevents the user from killing the script with Ctrl+C (KeyboardInterrupt)
    and intercepts system exit commands (sys.exit).
    """
    try:
        logging.info("Running unsafe loop... (Simulating sys.exit)")
        sys.exit(1)  # Simulating a system termination command
    except:
        # BAD: This catches the SystemExit signal and prevents the program from closing properly!
        logging.error("Caught an exception! The sys.exit command was blocked!")


def safe_standard_except():
    """
    ✅ PRODUCTION STANDARD: Catching 'Exception'.
    This catches application-level errors (ValueErrors, TypeErrors, CustomErrors)
    but allows SystemExit and KeyboardInterrupt to pass through cleanly.
    """
    try:
        logging.info("Running safe block... (Simulating sys.exit)")
        sys.exit(1)
    except Exception as e:
        # This block will NOT execute because SystemExit does not inherit from Exception.
        logging.error("This will not print during a SystemExit.")
    finally:
        logging.info("Safe block cleanup executed.")


if __name__ == "__main__":
    logging.info("--- Executing Exception Hierarchy Module ---")

    # 1. Demonstrate the flaw of the bare except
    unsafe_bare_except()

    # 2. Demonstrate the safety of catching 'Exception'
    try:
        safe_standard_except()
    except SystemExit:
        logging.info("SystemExit cleanly bypassed the 'except Exception' block as intended.")
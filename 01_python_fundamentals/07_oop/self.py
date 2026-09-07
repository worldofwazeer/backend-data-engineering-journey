"""
The explicit 'self' parameter mechanism.
Demonstrates how Python binds instance methods and translates calls under the hood.
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class PipelineWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id

    def report_status(self) -> str:
        """The 'self' parameter explicitly receives the instance upon invocation."""
        return f"Worker {self.worker_id} is idle."


if __name__ == "__main__":
    logging.info("--- Executing Self Module ---")

    worker = PipelineWorker(worker_id="WRK-99")

    # Standard Invocation (Syntactic Sugar)
    # Python automatically injects the 'worker' instance as the 'self' argument.
    standard_call = worker.report_status()

    # Explicit Unbound Invocation (Under the hood)
    # This is exactly what Python translates the above line into.
    explicit_call = PipelineWorker.report_status(worker)

    assert standard_call == explicit_call
    logging.info("Standard invocation matches explicit class-level invocation: %s", standard_call)
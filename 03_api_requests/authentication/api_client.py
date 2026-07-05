import logging
import time
from typing import Optional
import requests
from requests.exceptions import (
    HTTPError,
    RequestException,
)
from config import (
    API_KEY,
    BACKOFF_FACTOR,
    BASE_URL,
    MAX_RETRIES,
    TIMEOUT,
)

RETRY_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger("ETL_PRACTICE")


class APIClient:
    """
Reusable HTTP client that provides authentication, retry logic,
rate limiting, timeout handling, and JSON response validation.
"""

    def __init__(self) -> None:
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "WorldOfWazeerDataIngestion/1.0",
            "Accept": "application/json",
            "X-API-Key": API_KEY,
        })

    def get(self, endpoint: str, **kwargs) -> dict:
        url = f"{BASE_URL}{endpoint}"

        max_retries = MAX_RETRIES
        last_exception: Optional[Exception] = None

        for attempt in range(max_retries + 1):
            delay = BACKOFF_FACTOR ** attempt
            try:
                response = self.session.get(
                    url,
                    timeout=TIMEOUT,
                    **kwargs,
                )

                response.raise_for_status()

                # Step 1 & 2: Validate Content-Type Header
                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    logger.error(
                        "Expected JSON response but received %s",
                        content_type,
                    )
                    raise ValueError(
                        f"Expected JSON response, got {content_type}"
                    )

                # Step 3: Safely Parse JSON Payload
                try:
                    payload = response.json()
                    logger.info("GET %s succeeded.", endpoint)
                    return payload
                except requests.exceptions.JSONDecodeError:
                    logger.error(
                        "Invalid JSON payload received from %s",
                        endpoint,
                    )
                    raise

            except HTTPError as e:
                last_exception = e
                status_code = e.response.status_code

                if status_code not in RETRY_STATUS_CODES:
                    logger.error(
                        "HTTP %d is not retryable.",
                        status_code,
                    )
                    raise

                if status_code == 429:
                    retry_after = e.response.headers.get("Retry-After")

                    if retry_after is not None:
                        delay = int(retry_after)
                        logger.warning(
                            "Rate limit reached. Server requested %d second(s).",
                            delay,
                        )

                logger.warning(
                    "HTTP %d received. Retrying request...",
                    status_code,
                )

            except RequestException as e:
                last_exception = e
                logger.warning(
                    "Network error: %s",
                    e,
                )

            if attempt == max_retries:
                logger.error("Maximum retries exceeded.")
                if last_exception is not None:
                    raise last_exception
                raise RuntimeError("Maximum retries exceeded with unknown error.")

            logger.info(
                "Retrying in %d second(s)...",
                delay,
            )

            time.sleep(delay)

    def close(self) -> None:
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
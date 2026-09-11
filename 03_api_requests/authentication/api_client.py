import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
    Reusable HTTP client for authenticated API requests.

    Responsibilities:
    - Maintain a reusable HTTP session
    - Configure authentication and common headers
    - Apply HTTP retry policies
    - Validate HTTP responses
    - Parse JSON responses
    - Clean up the HTTP session
    """

    def __init__(self) -> None:
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "WorldOfWazeerDataIngestion/1.0",
            "Accept": "application/json",
            "X-API-Key": API_KEY,
        })

        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=RETRY_STATUS_CODES,
            allowed_methods=frozenset({
                "GET",
                "HEAD",
            }),
            respect_retry_after_header=True,
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, endpoint: str, **kwargs: Any) -> dict:
        """
        Send a GET request and return the JSON response.
        """

        url = f"{BASE_URL}{endpoint}"

        response = self.session.get(
            url,
            timeout=TIMEOUT,
            **kwargs,
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            "",
        )

        if "application/json" not in content_type:
            logger.error(
                "Expected JSON response but received %s",
                content_type,
            )

            raise ValueError(
                f"Expected JSON response, got {content_type}"
            )

        try:
            payload = response.json()

        except ValueError:
            logger.error(
                "Invalid JSON payload received from %s",
                endpoint,
            )
            raise

        logger.info(
            "GET %s succeeded.",
            endpoint,
        )

        return payload

    def close(self) -> None:
        """Close the HTTP session."""

        self.session.close()

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.close()
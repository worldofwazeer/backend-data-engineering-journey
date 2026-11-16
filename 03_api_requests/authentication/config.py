from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def _parse_int_setting(
    name: str,
    raw_value: str | None,
    *,
    default: int,
    minimum: int,
) -> int:

    if raw_value is None:
        raw_value = str(default)

    try:
        value = int(raw_value)

    except ValueError as exc:
        raise ValueError(
            f"{name} must be an integer."
        ) from exc

    if value < minimum:
        raise ValueError(
            f"{name} must be greater than or equal to {minimum}."
        )

    return value

TIMEOUT = _parse_int_setting(
    "TIMEOUT",
    os.getenv("TIMEOUT"),
    default=15,
    minimum=1,
)

MAX_RETRIES = _parse_int_setting(
    "MAX_RETRIES",
    os.getenv("MAX_RETRIES"),
    default=3,
    minimum=0,
)

BACKOFF_FACTOR = _parse_int_setting(
    "BACKOFF_FACTOR",
    os.getenv("BACKOFF_FACTOR"),
    default=2,
    minimum=0,
)

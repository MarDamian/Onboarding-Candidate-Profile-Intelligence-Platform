import logging
import os
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log
)

# Configure logging
logger = logging.getLogger(__name__)

retry_config = {
    "max_retries": int(os.getenv("MAX_RETRIES", 3)),
    "min_seconds": int(os.getenv("RETRY_MIN_WAIT", 1)),
    "max_seconds": int(os.getenv("RETRY_MAX_WAIT", 10))
}

def create_retry_decorator():
    """
    Creates a retry decorator with exponential backoff based on env vars.
    """
    return retry(
        stop=stop_after_attempt(retry_config["max_retries"]),
        wait=wait_exponential(multiplier=retry_config["min_seconds"], min=retry_config["min_seconds"], max=retry_config["max_seconds"]),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )

pipeline_retry = create_retry_decorator()

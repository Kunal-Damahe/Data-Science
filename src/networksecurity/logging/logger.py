import logging
from pathlib import Path

from networksecurity.constants import LOG_FILE_PATH, LOG_DIR


def _configure_logging() -> None:
    """Configure application-wide logging once."""
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            logging.StreamHandler(),
        ],
    )


_configure_logging()

logger = logging.getLogger("networksecurity")

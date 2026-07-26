import logging

from app.core.config import get_settings


def configure_logging() -> None:
    """Configure application-wide logging."""

    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

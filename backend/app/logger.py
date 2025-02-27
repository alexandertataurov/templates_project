"""
Centralized logging configuration with structured output and rotation.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
from app.config import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure application-wide logging with file and console handlers.

    Args:
        log_level: Optional override for the logging level
    """
    # Clear existing handlers
    root = logging.getLogger()
    root.handlers.clear()

    # Set log level from config or parameter
    level = getattr(logging, (log_level or settings.LOG_LEVEL).upper())

    # Create formatters
    console_formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)

    # Configure file handler with rotation
    file_handler = RotatingFileHandler(
        filename=settings.LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG if settings.DEBUG else level)

    # Set up root logger
    root.setLevel(level)
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # Create app logger
    app_logger = logging.getLogger("app")
    app_logger.setLevel(level)

    # Log initial configuration
    app_logger.info(
        "Logging configured - Level: %s, File: %s",
        logging.getLevelName(level),
        settings.LOG_FILE,
    )


# Initialize logging and define a reusable logger
setup_logging()
logger = logging.getLogger("app")  # Use a consistent name for the app logger


if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")

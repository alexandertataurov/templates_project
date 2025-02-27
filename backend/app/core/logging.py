"""
Advanced logging and journaling configuration.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from app.config import settings


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": str(record.exc_info[0]),
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data

        return json.dumps(log_data)


class ContextLogger(logging.Logger):
    """Logger with context support."""

    def __init__(self, name: str, level: int = logging.NOTSET):
        super().__init__(name, level)
        self.context: Dict[str, Any] = {}

    def bind(self, **kwargs: Any) -> None:
        """Add context data to logger."""
        self.context.update(kwargs)

    def _log(self, level: int, msg: str, args: tuple, **kwargs: Any) -> None:
        """Override log method to include context."""
        if self.context:
            extra = kwargs.get("extra", {})
            extra["extra_data"] = self.context
            kwargs["extra"] = extra
        super()._log(level, msg, args, **kwargs)


def setup_logging(
    log_level: str = "INFO", log_dir: Optional[Path] = None, app_name: str = "app"
) -> None:
    """
    Configure application logging with advanced features.

    Args:
        log_level: Logging level
        log_dir: Directory for log files
        app_name: Application name for log files

    Features:
        - JSON structured logging
        - Rotating file handlers
        - Separate error logs
        - Request/Response logging
        - Performance metrics
        - Context support
    """
    # Register custom logger
    logging.setLoggerClass(ContextLogger)

    # Create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(console_handler)

    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Main log file (JSON formatted)
        main_handler = RotatingFileHandler(
            log_dir / f"{app_name}.json", maxBytes=10_485_760, backupCount=5  # 10MB
        )
        main_handler.setFormatter(JsonFormatter())
        logger.addHandler(main_handler)

        # Error log file
        error_handler = TimedRotatingFileHandler(
            log_dir / f"{app_name}.error.log",
            when="midnight",
            interval=1,
            backupCount=30,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JsonFormatter())
        logger.addHandler(error_handler)

        # Access log file
        access_handler = TimedRotatingFileHandler(
            log_dir / f"{app_name}.access.log",
            when="midnight",
            interval=1,
            backupCount=30,
        )
        access_handler.setFormatter(JsonFormatter())
        logger.addHandler(access_handler)

    # Set debug mode
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")


def get_logger(name: str) -> ContextLogger:
    """Get a context-aware logger instance."""
    return logging.getLogger(name)

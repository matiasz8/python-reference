"""Structured logging for the Greenhouse API Proxy."""

import logging
import sys
from pathlib import Path
from typing import Optional

from config import LOG_LEVEL


def setup_logger(
    name: str = "greenhouse",
    log_file: Optional[Path] = None,
    level: str = LOG_LEVEL,
) -> logging.Logger:
    """Set up a structured logger for the application.

    Args:
        name: Logger name
        log_file: Optional log file path
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "greenhouse") -> logging.Logger:
    """Get a logger instance with default configuration."""
    return setup_logger(name)


# Default application logger
app_logger = get_logger("greenhouse.app")
api_logger = get_logger("greenhouse.api")
client_logger = get_logger("greenhouse.client")

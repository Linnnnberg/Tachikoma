"""
Logging configuration and utilities for Tachikoma.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> None:
    """Setup logging configuration for Tachikoma."""

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()), format=format_string, handlers=[]
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_formatter = logging.Formatter(format_string)
    console_handler.setFormatter(console_formatter)

    # Add console handler to root logger
    logging.getLogger().addHandler(console_handler)

    # File handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)

        # Add file handler to root logger
        logging.getLogger().addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(name)


class TachikomaLogger:
    """Custom logger class for Tachikoma with additional functionality."""

    def __init__(self, name: str):
        self.logger = get_logger(name)

    def log_agent_interaction(self, agent_id: str, action: str, details: str = ""):
        """Log agent interactions with structured format."""
        self.logger.info(f"AGENT[{agent_id}] {action}: {details}")

    def log_resource_allocation(
        self, agent_id: str, old_score: float, new_score: float
    ):
        """Log resource allocation changes."""
        self.logger.info(
            f"RESOURCE[{agent_id}] Score: {old_score:.2f} -> {new_score:.2f}"
        )

    def log_role_suggestion(self, suggestion: str, necessity_score: float):
        """Log role suggestions."""
        self.logger.info(f"SUGGESTION[{necessity_score:.2f}] {suggestion}")

    def log_system_event(self, event: str, details: str = ""):
        """Log system-level events."""
        self.logger.info(f"SYSTEM[{event}] {details}")

    def log_error(self, component: str, error: str, exc_info: bool = True):
        """Log errors with component context."""
        self.logger.error(f"ERROR[{component}] {error}", exc_info=exc_info)

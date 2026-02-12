"""Logging configuration utilities."""

from __future__ import annotations

import logging


def setup_logging(level: str = "INFO") -> None:
    """Configure basic logging for the CLI."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

"""Configuration helpers for environment-driven settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    api_base_url: str | None
    api_key: str | None


def get_settings() -> Settings:
    """Return settings from environment variables.

    Supported variables:
    - MR_API_BASE_URL
    - MR_API_KEY
    """
    return Settings(
        api_base_url=os.getenv("MR_API_BASE_URL"),
        api_key=os.getenv("MR_API_KEY"),
    )

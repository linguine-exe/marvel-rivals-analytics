"""Filesystem helpers for input discovery."""

from __future__ import annotations

from pathlib import Path


class FileDiscoveryError(ValueError):
    """Raised when expected input files cannot be found."""


def find_latest_raw_file(*, endpoint_slug: str, raw_dir: Path) -> Path:
    """Return latest timestamped raw JSON file for an endpoint."""
    if not raw_dir.exists():
        raise FileDiscoveryError(
            f"No raw data directory found at {raw_dir}. Run `fetch /{endpoint_slug}` first."
        )

    pattern = f"{endpoint_slug}_*.json"
    candidates = [
        path
        for path in raw_dir.glob(pattern)
        if path.is_file() and not path.name.endswith(".meta.json")
    ]

    if not candidates:
        raise FileDiscoveryError(
            f"No raw files found for /{endpoint_slug} in {raw_dir}. "
            f"Run `python -m marvel_rivals_analytics fetch /{endpoint_slug}` first."
        )

    return max(candidates, key=lambda path: path.stat().st_mtime)

"""Utilities for persisting raw API payloads and request metadata."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _timestamp_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def endpoint_slug(path: str) -> str:
    """Create a stable filename slug from an endpoint path."""
    cleaned = path.strip().strip("/")
    if not cleaned:
        return "root"
    return cleaned.replace("/", "_")


def save_raw_json(
    *,
    outdir: Path,
    endpoint: str,
    payload: dict,
    url: str,
    params: dict[str, str] | None,
    status_code: int,
) -> tuple[Path, Path]:
    """Persist JSON response and metadata sidecar in outdir."""
    outdir.mkdir(parents=True, exist_ok=True)
    timestamp = _timestamp_utc()
    stem = f"{endpoint_slug(endpoint)}_{timestamp}"

    data_path = outdir / f"{stem}.json"
    metadata_path = outdir / f"{stem}.meta.json"

    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    metadata = {
        "url": url,
        "params": params or {},
        "status_code": status_code,
        "saved_file": str(data_path),
        "timestamp_utc": timestamp,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return data_path, metadata_path


def save_request_metadata(
    *,
    outdir: Path,
    endpoint: str,
    url: str,
    params: dict[str, str] | None,
    status_code: int,
    response_text: str | None = None,
    saved_file: str | None = None,
) -> Path:
    """Persist request metadata for success and failure flows."""
    outdir.mkdir(parents=True, exist_ok=True)
    timestamp = _timestamp_utc()
    stem = f"{endpoint_slug(endpoint)}_{timestamp}"
    metadata_path = outdir / f"{stem}.meta.json"

    metadata = {
        "url": url,
        "params": params or {},
        "status_code": status_code,
        "saved_file": saved_file,
        "timestamp_utc": timestamp,
    }
    if response_text is not None:
        metadata["response_text"] = response_text[:500]

    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata_path

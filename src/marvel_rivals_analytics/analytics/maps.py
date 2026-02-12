"""Maps analytics transformations."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class MapsDataError(ValueError):
    """Raised when saved maps payloads cannot be processed."""


def load_maps_payload(infile: Path) -> dict | list:
    """Load and parse a saved maps JSON payload."""
    try:
        return json.loads(infile.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MapsDataError(f"Input file not found: {infile}") from exc
    except json.JSONDecodeError as exc:
        raise MapsDataError(
            f"Invalid JSON in {infile}. Hint: inspect the raw file contents."
        ) from exc


def _extract_records(payload: dict | list) -> list[dict]:
    """Extract a list of map records from common payload shapes."""
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        for key in ("data", "results", "maps", "items"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                records = candidate
                break
        else:
            if payload and all(not isinstance(value, (dict, list)) for value in payload.values()):
                records = [payload]
            else:
                raise MapsDataError(
                    "Unexpected maps JSON shape. Expected a list, or a dict containing "
                    "one of: data/results/maps/items as a list. Hint: inspect the raw file."
                )
    else:
        raise MapsDataError(
            "Unexpected maps JSON shape. Expected object or array. "
            "Hint: inspect the raw file."
        )

    if not all(isinstance(item, dict) for item in records):
        raise MapsDataError(
            "Unexpected maps JSON shape. Expected each map record to be an object. "
            "Hint: inspect the raw file."
        )

    return records


def normalize_maps(payload: dict | list) -> pd.DataFrame:
    """Normalize maps payload data into a flat dataframe."""
    records = _extract_records(payload)

    if not records:
        return pd.DataFrame()

    frame = pd.json_normalize(records, sep="_")
    frame.columns = [col.strip().replace(".", "_") for col in frame.columns]
    return frame


def build_maps_summary(maps_df: pd.DataFrame) -> pd.DataFrame:
    """Create simple summary metrics from normalized maps data."""
    rows: list[dict[str, int]] = [{"metric": "row_count", "value": int(len(maps_df))}]
    rows.append({"metric": "column_count", "value": int(len(maps_df.columns))})

    if maps_df.empty:
        return pd.DataFrame(rows)

    for column in maps_df.columns:
        rows.append({"metric": f"non_null_{column}", "value": int(maps_df[column].notna().sum())})

    candidate_name_columns = ["name", "map_name", "display_name", "title"]
    for column in candidate_name_columns:
        if column in maps_df.columns:
            rows.append(
                {
                    "metric": f"unique_{column}",
                    "value": int(maps_df[column].nunique(dropna=True)),
                }
            )

    return pd.DataFrame(rows)


def analyze_maps_to_csv(infile: Path, processed_dir: Path) -> tuple[Path, Path, int]:
    """Analyze maps JSON and write cleaned + summary CSV outputs."""
    payload = load_maps_payload(infile)
    maps_df = normalize_maps(payload)
    summary_df = build_maps_summary(maps_df)

    processed_dir.mkdir(parents=True, exist_ok=True)
    maps_csv = processed_dir / "maps.csv"
    summary_csv = processed_dir / "maps_summary.csv"

    maps_df.to_csv(maps_csv, index=False)
    summary_df.to_csv(summary_csv, index=False)

    return maps_csv, summary_csv, len(maps_df)

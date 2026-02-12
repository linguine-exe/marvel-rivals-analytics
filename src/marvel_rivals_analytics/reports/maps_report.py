"""Maps reporting utilities for portfolio-friendly markdown and charts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class MapsReportError(ValueError):
    """Raised when maps report inputs are missing or invalid."""


@dataclass(frozen=True)
class MapsReportArtifacts:
    """Generated report artifact paths and key metrics."""

    markdown_path: Path
    chart_path: Path
    timestamp_utc: str
    total_maps: int
    dimension_name: str
    top_counts: pd.Series


def _timestamp_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _pick_dimension_column(maps_df: pd.DataFrame) -> str:
    preferred_columns = ("mode", "category", "tag", "tags")
    for column in preferred_columns:
        if column in maps_df.columns:
            return column
    raise MapsReportError(
        "Could not find a report dimension column. Expected one of: mode, category, tag, tags "
        "in data/processed/maps.csv."
    )


def _load_processed_inputs(processed_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    maps_csv = processed_dir / "maps.csv"
    summary_csv = processed_dir / "maps_summary.csv"

    missing = [str(path) for path in (maps_csv, summary_csv) if not path.exists()]
    if missing:
        missing_str = ", ".join(missing)
        raise MapsReportError(
            "Missing processed maps files: "
            f"{missing_str}. Run `python -m marvel_rivals_analytics analyze maps` first."
        )

    return pd.read_csv(maps_csv), pd.read_csv(summary_csv)


def build_dimension_counts(maps_df: pd.DataFrame) -> tuple[str, pd.Series]:
    """Return the best available grouping column and value counts."""
    dimension_name = _pick_dimension_column(maps_df)
    counts = (
        maps_df[dimension_name]
        .fillna("<unknown>")
        .astype(str)
        .replace("", "<unknown>")
        .value_counts()
    )

    if counts.empty:
        raise MapsReportError("No rows available in maps.csv to build a report.")

    return dimension_name, counts


def save_maps_chart(counts: pd.Series, dimension_name: str, chart_path: Path) -> Path:
    """Generate and save a clean bar chart from grouped map counts."""
    chart_path.parent.mkdir(parents=True, exist_ok=True)

    plot_values = counts.head(10).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(plot_values.index, plot_values.values, color="#2563eb")
    ax.set_title(f"Maps by {dimension_name}")
    ax.set_xlabel("Map count")
    ax.set_ylabel(dimension_name)

    for idx, value in enumerate(plot_values.values):
        ax.text(value + 0.05, idx, str(int(value)), va="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(chart_path, dpi=150)
    plt.close(fig)
    return chart_path


def _render_markdown(
    *,
    timestamp_utc: str,
    total_maps: int,
    dimension_name: str,
    top_counts: pd.Series,
    chart_path: Path,
    markdown_path: Path,
) -> str:
    chart_relative = chart_path.name

    lines = [
        "# Maps Visual Report",
        "",
        f"- Timestamp (UTC): `{timestamp_utc}`",
        f"- Total maps: **{total_maps}**",
        f"- Grouped by: **{dimension_name}**",
        "",
        "## Top 3 Groups",
        "",
    ]

    for rank, (label, value) in enumerate(top_counts.head(3).items(), start=1):
        lines.append(f"{rank}. `{label}` — {int(value)} maps")

    lines.extend([
        "",
        "## Charts",
        "",
        f"- [{chart_path.name}]({chart_relative})",
        "",
        f"![Maps by {dimension_name}]({chart_relative})",
        "",
        f"_Report file: `{markdown_path.name}`_",
    ])

    return "\n".join(lines)


def generate_maps_report(processed_dir: Path, reports_dir: Path) -> MapsReportArtifacts:
    """Generate markdown + chart artifacts for processed maps analytics."""
    maps_df, _summary_df = _load_processed_inputs(processed_dir)
    dimension_name, counts = build_dimension_counts(maps_df)
    timestamp_utc = _timestamp_utc()

    reports_dir.mkdir(parents=True, exist_ok=True)
    chart_path = reports_dir / f"maps_by_mode_{timestamp_utc}.png"
    markdown_path = reports_dir / f"maps_report_{timestamp_utc}.md"

    save_maps_chart(counts=counts, dimension_name=dimension_name, chart_path=chart_path)

    markdown = _render_markdown(
        timestamp_utc=timestamp_utc,
        total_maps=int(len(maps_df)),
        dimension_name=dimension_name,
        top_counts=counts,
        chart_path=chart_path,
        markdown_path=markdown_path,
    )
    markdown_path.write_text(markdown, encoding="utf-8")

    return MapsReportArtifacts(
        markdown_path=markdown_path,
        chart_path=chart_path,
        timestamp_utc=timestamp_utc,
        total_maps=int(len(maps_df)),
        dimension_name=dimension_name,
        top_counts=counts.head(3),
    )

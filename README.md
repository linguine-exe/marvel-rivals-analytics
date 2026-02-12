# marvel-rivals-analytics
Data pipeline + dashboard exploring Marvel Rivals hero pick rates, win rates, and team composition trends.

# Marvel Rivals Analytics Dashboard

## Overview

This project builds a data analytics pipeline and interactive dashboard for analyzing **Marvel Rivals gameplay trends**.
The goal is to explore hero performance, match outcomes, team compositions, and evolving meta patterns using structured match data and live API integration.
This project is designed to simulate real-world game analytics workflows used in competitive multiplayer titles.

---

## What This Project Does

### Hero Meta Analysis
- Calculate **pick rates** across maps, modes, and ranks
- Compute **win rates** with proper sample size filtering
- Identify overperforming and underperforming heroes
- Track meta shifts over time

### Team Composition Insights
- Detect common hero pairings and trios
- Measure win rate impact of specific compositions
- Analyze role balance (Tank / DPS / Support distribution)
- Identify high-synergy combinations

### Map & Mode Performance
- Compare hero performance across maps
- Analyze control vs payload vs other mode differences
- Identify map-specific advantages

### Player Performance Tracking (Optional Module)
- Personal match tracking dashboard
- Trend lines for improvement over time
- Performance by hero, map, and role
- Efficiency metrics (KDA, damage per minute, etc.)

### Patch / Update Impact Analysis (Future Phase)
- Compare pre- and post-balance change performance
- Quantify meta shifts using rolling averages
- Detect statistically significant performance changes

---

## Analytics Techniques Used

- Grouped aggregation and normalization
- Rolling averages and trend smoothing
- Win rate confidence intervals
- Time series comparisons
- Basic modeling for trend forecasting
- Visualization-driven exploratory analysis

---

## Architecture

The project follows a modular structure:

- `data/` → Raw and processed match data
- `src/` → Metrics and analytics functions
- `notebooks/` → Exploratory analysis
- `dashboard/` (Phase 2) → Streamlit app

---

## Roadmap

**Phase 1**
- Finalize match schema
- Compute baseline hero pick + win rates
- Generate static visualizations

**Phase 2**
- Build interactive Streamlit dashboard
- Add filtering by map, rank, and mode
- Deploy locally

**Phase 3**
- Advanced synergy analysis
- Patch impact module
- Statistical significance testing
- Public deployment

---

## Why This Project Matters

Competitive multiplayer games rely heavily on data-driven balance decisions.  
This project demonstrates the ability to:

- Work with structured and semi-structured game data
- Build clean analytics pipelines
- Translate raw gameplay logs into actionable insights
- Design dashboards similar to those used by game studios

This repository serves as a portfolio-ready example of applied game analytics.

---

## Milestone 0: Project wiring (current)

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### CLI sanity checks

```bash
python -m marvel_rivals_analytics --help
python -m marvel_rivals_analytics ping
```

### Optional environment variables

```bash
export MR_API_BASE_URL="https://api.example.com"
export MR_API_KEY="your-api-key"
python -m marvel_rivals_analytics ping
```

## Milestone 1: Data fetching

Set API environment variables:

```bash
export MR_API_BASE_URL="https://marvelrivalsapi.com/api/v1"
export MR_API_KEY="your-real-api-key"
```

Dry run for `/maps` (prints URL and whether `x-api-key` is set, without calling the API):

```bash
python -m marvel_rivals_analytics fetch /maps --dry-run
```

Real fetch for `/maps`:

```bash
python -m marvel_rivals_analytics fetch /maps
```

Fetch with params:

```bash
python -m marvel_rivals_analytics fetch /maps --params region=global lang=en
```

Raw payloads and metadata sidecars are written to `data/raw/` by default.


## Milestone 2: Analytics (maps to CSV)

Fetch `/maps` raw JSON first:

```bash
python -m marvel_rivals_analytics fetch /maps
```

Analyze the latest saved maps payload (default behavior):

```bash
python -m marvel_rivals_analytics analyze maps
```

Analyze a specific raw input file:

```bash
python -m marvel_rivals_analytics analyze maps --infile data/raw/maps_YYYY-mm-ddTHH-MM-SSZ.json
```

You can also force latest-file selection explicitly:

```bash
python -m marvel_rivals_analytics analyze maps --latest
```

Outputs are written to `data/processed/`:

- `data/processed/maps.csv` (normalized table)
- `data/processed/maps_summary.csv` (counts and simple metrics)


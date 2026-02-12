# Marvel Rivals Analytics: Build Spec

## Goal
A Python project that can:
1) Fetch data from a Marvel Rivals API
2) Save raw responses to disk in a reproducible way
3) Build a small set of analytics summaries from saved data
4) Export results (CSV + simple charts) for portfolio use

## Non-goals (for now)
- Web app UI
- Database
- Authentication complexity beyond an API key in env vars
- Cloud deployment

## Inputs
- Environment variables:
  - MR_API_BASE_URL
  - MR_API_KEY (optional until needed)
- CLI arguments (planned):
  - `fetch ...`
  - `analyze ...`
  - `report ...`

## Outputs
- `data/raw/` saved JSON with timestamps and endpoint names
- `data/processed/` saved CSV
- `reports/` saved charts and a short markdown summary

## Definition of Done (MVP)
- `python -m marvel_rivals_analytics fetch <endpoint>` saves JSON to `data/raw/`
- `python -m marvel_rivals_analytics analyze` produces at least 1 CSV in `data/processed/`
- `python -m marvel_rivals_analytics report` creates a chart image in `reports/`
- README shows exact commands to run MVP end to end

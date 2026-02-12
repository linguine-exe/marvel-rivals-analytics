# Task List

## Milestone 0: Project wiring
- [ ] Add src-based package structure
- [ ] Add pyproject.toml
- [ ] Add CLI entry (python -m ...)
- [ ] Add config via env vars
- [ ] Add basic logging

## Milestone 1: Data fetching
- [ ] Add API client wrapper (requests)
- [ ] Add `fetch` CLI command
- [ ] Save raw JSON to data/raw/ with timestamped filenames
- [ ] Add a "dry run" mode (prints URL, does not call)

## Milestone 2: Analytics
- [ ] Add `analyze` command
- [ ] Load raw JSON and normalize to tables
- [ ] Output at least one CSV summary

## Milestone 3: Reporting
- [ ] Add `report` command
- [ ] Generate at least one chart image
- [ ] Write a short markdown summary in reports/

## Milestone 4: Polish
- [ ] Tests for key functions
- [ ] Makefile or scripts for common commands
- [ ] Improve README with examples

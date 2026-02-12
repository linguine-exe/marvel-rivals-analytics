# AGENTS

## Coding guidelines
- Use a src/ layout with a package named `marvel_rivals_analytics`.
- Keep changes small and easy to review.
- Do not delete existing files unless necessary.
- Add minimal docs as you go (update README when a command changes).
- Prefer standard libraries; use `requests`, `pandas`, `python-dotenv` only if needed.

## Project rules
- Raw API responses go to `data/raw/`
- Processed tables go to `data/processed/`
- Generated outputs go to `reports/`

## Definition of Done (Milestone 0)
- `python -m marvel_rivals_analytics --help` works
- `python -m marvel_rivals_analytics ping` works (even if it is a placeholder)
- Repo includes: src structure, pyproject.toml, .gitignore, basic config, basic logging

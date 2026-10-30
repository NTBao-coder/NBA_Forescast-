# NBA Forecast

Learning project for leakage-free forecasts of `P(home team wins)` in NBA games.

## Development

This project targets Python 3.12 and uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
uv run ruff check .
uv run nba-forecast --help
```

Source code lives in `src/nba_forecast/`; tests live in `tests/`. Raw API
responses belong in `data/raw/`, processed game-level data in
`data/processed/`, and committed live forecasts in `forecasts/`.
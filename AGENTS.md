# NBA Match Predictor

A learning project: forecast **P(home team wins)** for NBA games, with **live forecasting of the 2026–27 season** as the centrepiece. The owner is learning forecasting discipline; the code is a means to that.

Read `docs/CONTEXT.md` before any design, feature, model or plan work: it holds every settled decision, the glossary, and the open questions.

## Who writes what

The owner (Bảo) is learning pandas, scikit-learn and PyTorch on this project. Split the work by layer:

- **Agent writes the infra**: data fetching from `nba_api`, caching, retries, CLI wiring, CI.
- **Owner writes the core**: feature engineering, Elo, walk-forward validation, models, EDA. For core work, the agent provides function signatures, docstrings and failing `pytest` tests, then reviews and gives hints. Hand over a full core implementation only when the owner asks for it.

## Guardrail: leakage

Every feature for game *t* uses only games that finished before *t*. The leakage test suite enforces this; keep it green and extend it whenever a new feature lands.

## Conventions

Code, identifiers and commits in English. Explanations to the owner in Vietnamese.

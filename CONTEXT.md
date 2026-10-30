# Project context

Snapshot of the design interview, 2026-10-30. Settled decisions are binding until the owner changes them. Open questions carry a recommended default; treat them as unsettled until the owner answers.

## Goal

Learn **forecasting discipline**: leakage-free features, time-ordered validation, probabilistic evaluation. Comparing ML models is secondary. The headline deliverable is an honest, timestamped **live forecast record** of the 2026–27 regular season.

Owner background: solid probability and statistics, knows logistic regression theory; new to pandas, scikit-learn, PyTorch; comfortable with Git.

## Settled decisions

### Target and evaluation
- **Target**: P(home team wins) for a single game.
- **Primary metric**: log loss. Also report Brier score and a calibration plot. Accuracy is secondary only.
- **Baselines**, beaten in order before any ML model counts:
  - B0: constant historical home-win rate (~55–58%).
  - B1: season-to-date win% difference, using games before *t* only.
  - B2: Elo.

### Data
- Source: `nba_api` (stats.nba.com).
- Seasons: 2015–16 → 2025–26 for history, plus live 2026–27.
- Fetch once, cache in two layers: `data/raw/` holds API responses verbatim; `data/processed/` holds one row per game. The API returns one row per team per game, so pairs must be merged.
- Preseason: dropped. Regular season: used for training and evaluation. Playoffs: only update Elo, never evaluated.

### Validation
- **Walk-forward by season**: train on seasons ≤ N−1, validate on N, then slide forward.
- **2025–26 is the locked holdout**, scored exactly once at the end of backtesting.
- Live 2026–27 forecasts are the true out-of-sample test.

### Features
- Express every feature as **home − away**.
- Early season: rolling stats use `min_periods=1` plus a `games_played` feature.
- Head-to-head features are excluded (thin and noisy).
- Injuries/lineups (F6) are an extension: `nba_api` has no clean source.
- Feature-set focus is still open; see open question 1.

### Leakage rules
1. Rolling features use `shift(1)`, so game *t* never sits in its own window.
2. An automated test checks that changing the result of game *t* leaves the features of game *t* unchanged. The agent writes this test; the owner makes it pass.
3. Scalers and other preprocessing are `fit` on each fold's training data only.

### Elo
- Start from the FiveThirtyEight NBA setup:
  - K = 20, home advantage H = +100.
  - Margin-of-victory multiplier.
  - 25% reversion toward 1505 between seasons.
- Tune K (10–40) and H (40–140) by walk-forward log loss. Expect the tuned H to land below 100, since home advantage has shrunk since COVID.
- The formulas were explained to the owner in the interview; they implement Elo themselves.

### Models, in order
1. Logistic regression (scikit-learn).
2. Gradient boosting (LightGBM or `HistGradientBoostingClassifier`).
3. Small PyTorch MLP: 2 hidden layers, dropout, early stopping.

The likely, and acceptable, finding is that the MLP does not beat logistic regression on ~12k tabular rows.

### EDA (owner wants this thorough; one chart per question)
1. Home-court advantage by season; does it drop after COVID?
2. Distribution of point margins.
3. Effect of rest days and back-to-backs on win rate.
4. How strongly last-10-game form predicts the next result.
5. Elo trajectories for selected teams.
6. Correlation between features (redundancy).

### Stack and layout
- Python 3.12, `uv`, Git/GitHub, `pytest`, matplotlib/seaborn.
- Structured project: tested modules under `src/`; notebooks for EDA and charts only.

### Schedule
- 6 weeks, 6–8 h/week, starting Monday 2026-11-02.
- A week-by-week plan is still to be written. Restructure it around live forecasting starting early; see open question 2.

## Open questions

1. **Feature focus.** The owner wants F2 (efficiency: ORtg/DRtg, pace, Four Factors) and "F3". It is unclear whether "F3" means schedule features (rest days, back-to-back, road-trip length) or injuries. Recommended: F2 + F3 schedule + F4 Elo (needed early season); F1 rolling form optional.
2. **When live forecasting starts.** Recommended: Elo-only forecasts from week 1–2, upgrading models over time, with each forecast tagged by `model_version`.
3. **Forecast cadence.** Recommended: daily via GitHub Actions, run in the Vietnam evening (games tip off around 06:00–10:00 VN time). stats.nba.com often blocks cloud IPs, so verify early and fall back to a one-command local run.
4. **Proof of timing.** Recommended: append-only `forecasts/2026-27.csv`, committed before tip-off. Columns: `game_id, date, home, away, p_home, model_version, forecast_ts`. A scoring script joins it to results.
5. **Live results display.** Recommended: auto-updated README charts showing cumulative log loss per model vs baselines, plus calibration.
6. **Report language** (English vs Vietnamese). Undecided.
7. **The owner's own plan** matched ~80% of the agreed design. The other 20% has not been discussed yet.

## Glossary

- **Leakage**: any information from game *t* or later reaching the features or fit used to predict game *t*.
- **Walk-forward**: time-ordered validation that always trains on the past and tests on the next period.
- **Locked holdout**: data scored once, after all tuning; 2025–26 here.
- **Live forecast**: a prediction committed before tip-off for a game not yet played.
- **Elo**: rating in which expected P = 1 / (1 + 10^(−(R_home + H − R_away)/400)), updated as R ← R + K·(result − P).
- **K**: Elo update speed. **H**: Elo home-court bonus.
- **Four Factors**: eFG%, TOV%, OREB%, FT rate (Dean Oliver).
- **Back-to-back**: playing on consecutive days.
- **Calibration**: whether events forecast at p% happen about p% of the time.

# Competition Rules

## The Task

Build a daily, cross-sectional long/short equity strategy for an anonymized
universe of stocks, using the pre-computed features in `data/features.parquet`.
No raw price data (open/high/low/close) is provided — only derived indicators.

Your strategy is implemented as a single function, `get_weights`, completed in
`notebooks/main.ipynb`. It is called once per trading day and must return a
dictionary of stock positions for that day.

## Data Access Rules

- **Features:** the derived indicators in `data/features.parquet`.
- **Returns:** `data/returns.parquet` is provided **for local backtesting and
  validation only.**
- **`returns` may never be used as a model input.** It exists solely so you can
  score your own strategy before submitting. Final ranking is computed by the
  organizers over the official evaluation window.
- **No look-ahead.** When `get_weights` is called for date `t`, it only receives
  feature history strictly before `t`. Do not use information that wouldn't have
  been available at the time (anything dated `>= t`).

## Portfolio Constraints

For date `t` and stock `s`, let `w(t, s)` be the fraction of unit capital
allocated to that stock (positive = long, negative = short).

| Constraint | Rule |
|---|---|
| Unit capital | `sum(\|w[t, s]\|) <= 1 + 1e-4` |
| Max position size | `\|w[t, s]\| <= 0.1` for every stock |
| Dollar neutral | `\|sum(w[t, s])\| <= 1e-4` |
| Universe | `w[t, s] = 0` whenever `universe[t, s] = 0` |

A submission violating any of these will not be scored. Run the **validation
cell** in `notebooks/main.ipynb` (which calls `utils.validate_weights`) before
submitting to check all four automatically.

## Submission Integrity

- Your submitted code must reproduce the `submission.csv` you hand in. Mismatches
  between code and submission disqualify the entry.
- Only your **last** valid submission before the deadline counts.

## What's Allowed

- Any modeling approach: rule-based signals, statistical models, machine
  learning — your choice.
- Combining/transforming the provided features however you like.

## What's Not Allowed

- Using `returns.parquet` as a feature.
- Using future feature values (anything dated `>= t`) inside `get_weights` for date `t`.
- Submitting weights for stocks not in that day's `universe`.
- Using external data sources — only the provided anonymized features may be used.

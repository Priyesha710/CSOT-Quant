# Quant CSOT Week 3 Alpha Research Challenge

## Overview

In this challenge you will engage in alpha research to develop systematic
strategies for trading stocks on a daily basis using price and volume derived
features.

The objective is to identify predictive signals and construct a market-neutral
long-short portfolio that maximizes Net Sharpe Ratio.

---

## Timeline

| Event                   | Date              |
|-------------------------|-------------------|
| Competition Opens       | 16 June           |
| Competition Closes      | 23 June           |
| Final Submission Deadline | 23 June 11:59 PM |

---

## Dataset

The datasets are provided separately through Google Drive:

https://drive.google.com/drive/folders/1oE8A3YCEcDeTiv9Yc2QtzEUBX2XyLDtW?usp=sharing

Download and place the files inside:

```
data/
```

Expected files:

- features.parquet
- returns.parquet
- universe.parquet

See [`data/download_data.md`](data/download_data.md) for step-by-step download
instructions.

---

## Data Description

Features are derived from:

- Open
- High
- Low
- Close
- Volume

for 2167 anonymized stocks.

Date range: 2005-01-03 → 2025-02-07

Available Features:

- relative_strength_index
- williams_r
- volatility_20
- volatility_60
- trend_1_3
- trend_5_20
- trend_20_60
- average_true_range
- macd
- trix
- commodity_channel_index
- chande_momentum_oscillator
- ichimoku
- know_sure_thing
- ultimate_oscillator
- aroon
- stochastic_oscillator
- on_balance_volume
- ease_of_movement
- chaikin_money_flow
- accumulation_distribution_index
- volume

---

## Constraints

### Universe Constraint
Trade only stocks with `universe == 1`.

### Dollar Neutral Constraint
Long exposure must equal short exposure.

### Diversification Constraint
Avoid excessive concentration.

### No Lookahead Bias
Only information available up to t−1 may be used.

See [`docs/competition_rules.md`](docs/competition_rules.md) for the exact
numerical tolerances.

---

## Evaluation

The primary metric is:

Annualized Net Sharpe Ratio

```
NetPnL = GrossPnL − TradingCosts
Trading Cost = 0.01% × Traded Capital
```

Higher Net Sharpe indicates better performance. Full details in
[`docs/evaluation.md`](docs/evaluation.md).

---

## Submission Requirements

Submit:

- submission.csv
- strategy_description.txt
- source code repository

Format details are in [`docs/submission_format.md`](docs/submission_format.md).

---

## Repository Files

- `notebooks/main.ipynb` — contains the `get_weights()` implementation.
- `requirements.txt` — Python dependencies.
- `strategy_description_template.txt` — template for documenting strategy rationale.
- `src/utils.py` — backtest loop, metrics, and constraint checks.
- `sample_submission/submission.csv` — correctly-shaped example submission.
- `docs/` — rules, evaluation, submission format, and FAQ.

## Quick Start

```bash
pip install -r requirements.txt
# download the dataset into data/  (see data/download_data.md)
jupyter notebook notebooks/main.ipynb
```

The notebook loads the three parquet files, runs the backtest day by day using
your `get_weights` function, validates the portfolio constraints, reports
Gross/Net Sharpe and turnover, and writes `submission.csv`.

---

## Good Luck

Develop robust, interpretable, and scalable alpha signals.

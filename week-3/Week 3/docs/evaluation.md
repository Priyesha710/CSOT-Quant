# Evaluation

Strategies are scored on **Net Sharpe Ratio** — risk-adjusted returns after
trading costs. Higher is better.

## Derived Metrics

Given your daily weight matrix `w[t, s]`:

- **Book Value** — capital deployed that day:
  `BookValue[t] = sum(|w[t, s]|)`

- **Traded Capital** — capital turned over that day:
  `Traded[t] = sum(|w[t, s] - w[t-1, s]|)`

- **Turnover** — average daily capital traded as a % of book value:
  `Turnover = sum(Traded) / sum(BookValue) * 100`

- **Gross PnL** — daily portfolio return before costs:
  `GrossPnL[t] = sum(w[t, s] * returns[t, s])`

- **Net PnL** — daily portfolio return after costs (flat 0.01% of traded
  capital per day, charged to the broker):
  `NetPnL[t] = GrossPnL[t] - 0.01% * Traded[t]`

## Sharpe Ratios

Both are annualized using `sqrt(252)`:

```
Gross Sharpe = sqrt(252) * mean(GrossPnL) / std(GrossPnL)
Net Sharpe   = sqrt(252) * mean(NetPnL) / std(NetPnL)
```

**Net Sharpe Ratio is the metric that determines final ranking.**

## Training vs. Test Period

- You have returns for 2005–2019 to develop and validate locally — treat this
  as your training/validation period.
- Final scoring happens on a later, held-out period for which you do **not**
  have returns. Use cross-validation and out-of-sample checks during
  development rather than over-fitting to the visible Sharpe number — a
  strategy that only looks good on 2005–2019 data is unlikely to hold up.

All of these are implemented in `src/utils.py` (`book_value`, `traded_capital`,
`turnover`, `gross_pnl`, `net_pnl`, `sharpe_ratio`, `summarize_performance`) and
exercised in `notebooks/main.ipynb`.

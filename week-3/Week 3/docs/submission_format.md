# Submission Format

## `get_weights` Function

You implement this in `notebooks/main.ipynb`:

```python
def get_weights(features: pd.DataFrame, today_universe: pd.Series) -> dict[str, float]:
    """
    features        : history of all feature DataFrames, strictly before today
                       (MultiIndex columns: (feature_name, stock_id))
    today_universe   : 0/1 Series indexed by stock id — which stocks are
                       tradable today

    returns          : dict mapping stock id (str) -> weight for today.
                       Only include stock ids where today_universe == 1.
    """
```

It is called once per date by the backtest loop (`utils.backtest_strategy`),
which assembles every day's output into one weights matrix.

## `submission.csv`

The final deliverable is a CSV with:

- **Rows** — every date present in `data/universe.parquet`, no more, no fewer.
- **Columns** — every stock identifier present in `data/universe.parquet`, in
  the same order.
- **Values** — the float weight `w(t, s)` for each date/stock pair. `0` for any
  stock not tradable that day.

See `sample_submission/submission.csv` for a minimal example with the correct
shape (all-zero weights — it satisfies every constraint trivially but carries no
strategy, just shows the expected format).

## Validating Before You Submit

Run the **Validate constraints** cell in `notebooks/main.ipynb`. It calls
`utils.validate_shape` and `utils.validate_weights`, checking the shape against
`universe.parquet` and all four portfolio constraints from
`docs/competition_rules.md`, printing PASS/FAIL for each.

You can also validate from a script:

```python
import sys; sys.path.append("src")
import pandas as pd, utils
universe = pd.read_parquet("data/universe.parquet")
weights  = pd.read_csv("submission.csv", index_col=0, parse_dates=True)
weights.columns = weights.columns.astype(universe.columns.dtype)
print({**utils.validate_shape(weights, universe), **utils.validate_weights(weights, universe)})
```

## What to Submit

1. `notebooks/main.ipynb` with a completed `get_weights` function
2. `submission.csv` in the format above
3. `strategy_description.txt` — fill in `strategy_description_template.txt` with
   your reasoning
4. Your source code repository

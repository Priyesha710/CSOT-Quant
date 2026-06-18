"""
utils.py
--------
Helper functions for running, validating, and scoring a daily long/short
portfolio strategy against the constraints described in docs/competition_rules.md.

Paths default relative to this file's location (repo_root/src/utils.py), so
these functions work the same whether you call them from notebooks/, the
repo root, or a CI job.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"

TRADING_DAYS_PER_YEAR = 252
COST_BPS = 0.0001  # 0.01% trading cost per unit of traded capital
MAX_WEIGHT = 0.1
UNIT_CAPITAL_TOL = 1e-4
DOLLAR_NEUTRAL_TOL = 1e-4


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #

def load_data(
    features_path: str | Path = DATA_DIR / "features.parquet",
    universe_path: str | Path = DATA_DIR / "universe.parquet",
    returns_path: str | Path = DATA_DIR / "returns.parquet",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the three parquet files described in docs/submission_format.md."""
    features = pd.read_parquet(features_path)
    universe = pd.read_parquet(universe_path)
    returns = pd.read_parquet(returns_path)
    return features, universe, returns


# --------------------------------------------------------------------------- #
# Backtest loop
# --------------------------------------------------------------------------- #

def backtest_strategy(
    get_weights_fn,
    features: pd.DataFrame,
    universe: pd.DataFrame,
    show_progress: bool = True,
) -> pd.DataFrame:
    """
    Walk forward through every date in `universe`, calling `get_weights_fn`
    with only the feature history strictly before that date, and assemble
    the resulting daily weights into a single DataFrame.

    Parameters
    ----------
    get_weights_fn : callable(features: pd.DataFrame, today_universe: pd.Series) -> dict[str, float]
    features        : pd.DataFrame with MultiIndex columns (feature_name, stock_id)
    universe        : pd.DataFrame, same row index/columns as a single feature slice,
                       values in {0, 1}

    Returns
    -------
    pd.DataFrame of weights, same shape/index/columns as `universe`, filled with 0
    wherever a stock wasn't returned by `get_weights_fn` or wasn't in the universe.
    """
    dates = universe.index
    stock_ids = universe.columns
    weights = pd.DataFrame(0.0, index=dates, columns=stock_ids)

    iterator = tqdm(dates, desc="Backtesting") if show_progress else dates
    for t in iterator:
        history = features.loc[features.index < t]
        today_universe = universe.loc[t]

        raw_weights = get_weights_fn(history, today_universe)

        for stock_id, w in raw_weights.items():
            # Only accept weights for stocks that are actually tradable today.
            if stock_id in stock_ids and today_universe.get(stock_id, 0) == 1:
                weights.loc[t, stock_id] = w

    return weights


# --------------------------------------------------------------------------- #
# Constraint validation
# --------------------------------------------------------------------------- #

def validate_weights(weights: pd.DataFrame, universe: pd.DataFrame) -> dict[str, bool]:
    """
    Check the weight matrix against every constraint in docs/competition_rules.md.
    Returns a dict of constraint_name -> passed (bool).
    """
    book_value = weights.abs().sum(axis=1)
    max_abs_weight = weights.abs().max(axis=1)
    net_exposure = weights.sum(axis=1).abs()
    universe_violation = (weights.abs() * (1 - universe)).sum(axis=1)

    return {
        "unit_capital": bool((book_value <= 1 + UNIT_CAPITAL_TOL).all()),
        "max_weight": bool((max_abs_weight <= MAX_WEIGHT + 1e-9).all()),
        "dollar_neutral": bool((net_exposure <= DOLLAR_NEUTRAL_TOL).all()),
        "universe_respected": bool((universe_violation <= 1e-9).all()),
    }


def validate_shape(weights: pd.DataFrame, universe: pd.DataFrame) -> dict[str, bool]:
    """Check that a submission has exactly the rows/columns of universe.parquet."""
    return {
        "same_columns": list(weights.columns) == list(universe.columns),
        "same_index": list(weights.index) == list(universe.index),
        "no_missing_values": bool(weights.notna().all().all()),
    }


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #

def book_value(weights: pd.DataFrame) -> pd.Series:
    return weights.abs().sum(axis=1)


def traded_capital(weights: pd.DataFrame) -> pd.Series:
    return weights.diff().abs().sum(axis=1).fillna(weights.iloc[0].abs().sum())


def turnover(weights: pd.DataFrame) -> float:
    traded = traded_capital(weights)
    book = book_value(weights)
    return float(traded.sum() / book.sum() * 100)


def gross_pnl(weights: pd.DataFrame, returns: pd.DataFrame) -> pd.Series:
    common_idx = weights.index.intersection(returns.index)
    common_cols = weights.columns.intersection(returns.columns)
    w = weights.loc[common_idx, common_cols]
    r = returns.loc[common_idx, common_cols]
    return (w * r).sum(axis=1)


def net_pnl(weights: pd.DataFrame, returns: pd.DataFrame) -> pd.Series:
    g_pnl = gross_pnl(weights, returns)
    traded = traded_capital(weights).reindex(g_pnl.index).fillna(0)
    return g_pnl - COST_BPS * traded


def sharpe_ratio(pnl: pd.Series, annualization: int = TRADING_DAYS_PER_YEAR) -> float:
    std = pnl.std()
    if std == 0 or np.isnan(std):
        return 0.0
    return float(np.sqrt(annualization) * pnl.mean() / std)


def summarize_performance(weights: pd.DataFrame, returns: pd.DataFrame) -> dict[str, float]:
    """Convenience wrapper returning the full set of metrics from docs/evaluation.md."""
    g_pnl = gross_pnl(weights, returns)
    n_pnl = net_pnl(weights, returns)
    return {
        "turnover_pct": turnover(weights),
        "gross_sharpe": sharpe_ratio(g_pnl),
        "net_sharpe": sharpe_ratio(n_pnl),
        "mean_book_value": float(book_value(weights).mean()),
    }

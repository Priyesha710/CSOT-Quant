# CSOT Quant Finance & Research (Week 2)

## ML-Based Return Prediction

Last week you built intuition for markets, signals, and backtesting. You measured a hand-crafted signal against a buy-and-hold benchmark and learned that most signals are weak and noisy.

This week you'll approach the same problem from a different angle: **let the data tell you what predicts returns.** Instead of writing rules by hand, you'll use machine learning to learn patterns from historical features and predict future returns on unseen data.

By the end of this week you will:
1. Understand how supervised ML works (regression specifically)
2. Know how to engineer features from raw price data — and why this matters more than model choice
3. Be able to train, evaluate, and compare ML models for financial prediction
4. Submit predictions on a held-out test set and receive an R² score

---

## Prerequisites

From Week 1 you should be comfortable with:
- Daily returns (log returns, percentage returns)
- What a signal is and how to evaluate one
- Basic Python, Pandas, and Jupyter/Colab usage
- `yfinance`, `matplotlib`, rolling windows

---

## Week Structure

Work through the phases in order. Each one feeds the next.

| # | Phase | Time | Content |
|---|-------|------|---------|
| 1 | [ML Foundations](1-ml-foundations.md) | ~2 hours | What ML is, supervised learning, regression, overfitting, R² |
| 2 | [Feature Engineering](2-feature-engineering.md) | ~3 hours | Derived signals, technical indicators, lag features, leakage |
| 3 | [ML Models](3-models.md) | ~3 hours | Linear regression, trees, random forests, XGBoost, validation |
| — | [Project](project/README.md) | Rest of week | Predict returns on test data, submit CSV, get scored |

**Total time:** ~8–10 hours learning + project work.

---

## Setup

Everything you need:

```bash
pip install pandas numpy scikit-learn xgboost lightgbm matplotlib seaborn
```

Or use **Google Colab** — most of the libraries above are usually available already. If a package such as `lightgbm` is missing, install it in a cell with `!pip install lightgbm`.

If working locally and you don't have Jupyter:
```bash
pip install notebook
jupyter notebook
```

---

## How This Week Works

1. **Phases 1–3 are learning.** Read the material, watch the videos, build intuition. There are no graded deliverables in the phases — they exist to prepare you for the project.

2. **The project is the deliverable.** You'll receive a dataset with pre-computed features and a target column. Train a model, predict on the test set, submit a CSV. Your R² score on hidden data is your leaderboard position.

---

*Note: If you find any errors in this document, our apologies, and we would appreciate it if you let us know!*

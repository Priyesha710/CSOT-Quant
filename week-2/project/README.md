# Week 2 Project: Predict Stock Returns

## Overview

You are given a dataset of historical stock data with pre-computed features and a target column representing forward returns. Your task: **build an ML model that predicts returns on unseen data as accurately as possible.**

Your predictions will be scored by **R-squared (R²)** against the actual returns on a hidden test set. This is your leaderboard score.

---

## Dataset

The data lives in the `data/` folder:

| File | Description |
|------|-------------|
| `train.csv` | Training data — features + target column. Use this to train your model. |
| `test.csv` | Test data — same features, **no target column**. Predict the target for these rows. |
| `sample_submission.csv` | Shows the expected format for your submission. |

### Target Column

The target column is `target` — it represents the forward N-day return (continuous value, can be positive or negative).

For this project, interpret that as:

```text
target_t = (Close_{t+N} / Close_t) - 1
```

That means the row for day `t` may use features known by the end of day `t`, and the label measures the return from close `t` to close `t+N`. You should not use information from `t+1` or later when building features for row `t`.

### Feature Columns

The dataset contains raw OHLCV columns plus a small set of pre-computed features. Every column is described below.

| Column | Type | Meaning |
|--------|------|---------|
| `id` | int | Unique row identifier — use this in your submission. Not a predictor. |
| `Date` | date | Trading date for the observation. |
| `Open` / `High` / `Low` / `Close` | float | Daily OHLC prices. |
| `Volume` | float | Daily traded volume. |
| `feature_ret_1d` | float | 1-day past return, `Close_t / Close_{t-1} − 1`. |
| `feature_ret_5d` | float | 5-day past return, `Close_t / Close_{t-5} − 1`. |
| `feature_sma_20_ratio` | float | Close relative to its 20-day simple moving average, `Close / SMA(20)`. |
| `feature_vol_ratio_20d` | float | Volume relative to its 20-day average. |
| `feature_high_low_spread` | float | Intraday range, `(High − Low) / Close`. |
| `target` | float | **Train only.** Forward 10-day return, `Close_{t+10} / Close_t − 1`. |

All provided features are computed using only data available at prediction time (no leakage in the provided features). You're free to engineer additional features from these columns — just keep them backward-looking.

### Data Format

- Each row is one observation (one day for one asset)
- The `id` column uniquely identifies each row — use this in your submission
- Features are numeric (float).

---

## Your Task

1. **Explore the data** — distributions, correlations, missing values, outliers
2. **Select/engineer features** — you can use the provided features as-is, create new ones from them, or drop ones you think are noise
3. **Train at least 2 different models** — compare them (e.g. Linear Regression vs XGBoost)
4. **Generate predictions** on `test.csv`
5. **Submit** your predictions as a CSV file

---

## Submission Format

Your submission must be a CSV with exactly two columns:

```csv
id,predicted_target
0,0.00234
1,-0.00156
2,0.00089
...
```

- `id` must match the `id` column in `test.csv` exactly
- `predicted_target` is your model's predicted return for that row
- No headers other than `id,predicted_target`
- No missing values — every row in `test.csv` must have a prediction

See `data/sample_submission.csv` for the exact format.

---

## Scoring

Your score = **R² (R-squared)** between your `predicted_target` and the actual hidden target values.

```
R² = 1 - Σ(actual - predicted)² / Σ(actual - mean(actual))²
```

| R² | Interpretation |
|----|---------------|
| > 0.05 | Strong for financial data — you found real signal |
| 0.01 – 0.05 | Decent — your model captures some structure |
| ~0 | No better than predicting the mean |
| < 0 | Worse than predicting the mean — likely overfitting or bug |

You can test your model locally using the scoring script in `scoring/score.py` — but only on your own train/validation split (you don't have the test answers).

---

## Beginner Workflow

If you're not sure where to start, follow these steps:

### Step 1: Load and explore

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

print(train.shape)
print(train.describe())
print(train.isnull().sum())

# Target distribution
train['target'].hist(bins=50)
plt.title('Target Distribution')
plt.show()
```

### Step 2: Prepare features and target

```python
target_col = 'target'
id_col = 'id'
feature_cols = [c for c in train.columns if c not in [target_col, id_col]]

X_train = train[feature_cols]
y_train = train[target_col]
X_test = test[feature_cols]
```

### Step 3: Train a baseline model

```python
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline

model = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('regressor', LinearRegression())
])

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X_train):
    model.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
    val_pred = model.predict(X_train.iloc[val_idx])
    print(f"Fold R²: {r2_score(y_train.iloc[val_idx], val_pred):.4f}")

# After validation, fit on the full training data before predicting on test
model.fit(X_train, y_train)
```

### Step 4: Try a better model

```python
from xgboost import XGBRegressor

model = XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.05)
model.fit(X_train, y_train)
```

### Step 5: Generate predictions and submit

```python
predictions = model.predict(X_test)

submission = pd.DataFrame({
    'id': test['id'],
    'predicted_target': predictions
})
submission.to_csv('my_submission.csv', index=False)
```

---

## Common Mistakes

| Mistake | Why it's bad | Fix |
|---------|-------------|-----|
| Random train/test shuffle | Leaks future data into training | Use time-ordered split or `TimeSeriesSplit` |
| Not handling NaN | Model crashes or produces NaN predictions | Fit an imputer on the training fold only, ideally inside a `Pipeline` |
| Using `id` as a feature | It's an identifier, not a predictor | Exclude from feature columns |
| Training on test data | Circular — inflates score to meaninglessness | Never call `.fit()` with test data |
| Submitting wrong format | Score computation fails | Match `sample_submission.csv` exactly |
| Overfitting to training R² | Model memorises noise | Check validation R² — if train R² >> val R², reduce complexity |

---

## Tips for Improving Your Score

Once you have a working baseline, try these (roughly in order of impact):

1. **Feature selection** — remove features with near-zero importance or high correlation with each other. Fewer good features > many noisy ones.

2. **Create new features** — interactions (feature_A × feature_B), ratios, polynomial terms. Domain knowledge from Phase 2 helps here.

3. **Tune hyperparameters** — use `GridSearchCV` or `RandomizedSearchCV` with `TimeSeriesSplit`. Focus on `max_depth` and `learning_rate` first.

4. **Try ensembling** — average predictions from multiple models (e.g. 0.5 × XGBoost + 0.5 × LightGBM). Often beats any single model.

5. **Analyse residuals** — where is your model most wrong? Are there patterns in the errors that suggest missing features?

6. **Remove outliers from training** — extreme return days may be noise that hurts model training. Try clipping targets at ±3 standard deviations.

---

## Evaluation Rubric

| Component | Weight | What we look for |
|-----------|--------|-----------------|
| **R² score** (leaderboard) | 50% | Higher is better. This is your primary ranking metric. |
| **Notebook quality** | 30% | EDA, feature reasoning, model comparison, code clarity |
| **Honest assessment** | 20% | What worked, what didn't, why you chose your final model, what you'd try with more time |

> A high R² with no explanation scores lower than a moderate R² with clear reasoning about what you tried, what failed, and why your final model works. The leaderboard is a game; understanding is the goal.

---

## Submission Checklist

- [ ] Predictions generated for ALL rows in `test.csv` (no missing IDs)
- [ ] CSV format matches `sample_submission.csv` exactly
- [ ] No NaN or Inf values in predictions
- [ ] Notebook submitted alongside CSV showing your full workflow
- [ ] At least 2 models compared (even if one is just linear regression)
- [ ] Brief written section explaining your approach and results

---

## Local Scoring (for validation)

You can use `scoring/score.py` to test your submission format and score against your own validation split:

```bash
python scoring/score.py --predictions my_validation_preds.csv --actuals my_validation_actuals.csv
```

This helps you verify the format is correct before submitting. Your final score will be computed on the hidden test targets that you don't have access to.

---

**Good luck. Start simple, iterate fast, and understand your numbers.**

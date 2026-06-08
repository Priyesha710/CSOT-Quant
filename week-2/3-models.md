# Phase 3: ML Models That Work

*~3 hours | From baseline to competitive*

---

## The Models You'll Use

We'll cover four models in order of complexity. Start with the simplest (linear regression) and work up. In practice, you'll compare all of them on your data and pick the one that generalises best.

---

## 1. Linear Regression — Your Baseline

The simplest model: find a weighted combination of features that minimises prediction error.

```
predicted_return = w₁×feature₁ + w₂×feature₂ + ... + wₙ×featureₙ + bias
```

The model learns the weights (w₁, w₂, ...) from training data.

**Strengths:**
- Fast to train, easy to interpret
- Coefficients directly tell you feature importance (positive = feature predicts positive returns)
- Hard to overfit with few features

**Weaknesses:**
- Assumes linear relationships (if return = feature² this won't capture it)
- Sensitive to outliers and feature scale
- Can't model interactions between features

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Feature importance = coefficients
for name, coef in zip(feature_names, model.coef_):
    print(f"{name}: {coef:.6f}")
```

**When to use:** Always. This is your baseline. If a fancier model can't beat linear regression, the fancier model is overfitting.

**Watch:** [StatQuest: Linear Regression](https://www.youtube.com/watch?v=nk2CQITm_eo) (~12 min)

---

## 2. Decision Trees — Visual Intuition

A decision tree splits the data by asking sequential yes/no questions about features:

```
Is RSI > 70?
├── Yes: Is volatility > 0.02?
│   ├── Yes: predict -0.003
│   └── No: predict -0.001
└── No: Is momentum_5d > 0?
    ├── Yes: predict +0.002
    └── No: predict +0.0005
```

The tree learns which features to split on, what thresholds to use, and what value to predict at each leaf.

**Strengths:**
- Can capture non-linear patterns and interactions
- No feature scaling needed
- Easy to visualise and explain

**Weaknesses:**
- Extremely prone to overfitting (a deep tree memorises training data)
- High variance — small changes in data can produce very different trees
- Usually worse than ensembles

```python
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(max_depth=5)  # limit depth to prevent overfitting
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

**When to use:** Mostly for intuition. Rarely the best model on its own, but understanding trees is required to understand the next two models.

**Watch:** [StatQuest: Decision Trees](https://www.youtube.com/watch?v=_L39rN6gz7Y) (~18 min)

---

## 3. Random Forest — Wisdom of the Crowd

A Random Forest trains many decision trees on different random subsets of the data, then averages their predictions.

**Why this works:** Each individual tree overfits to its subset, but they overfit in different ways. Averaging cancels out the noise and keeps the signal.

This is called **bagging** (Bootstrap Aggregating):
1. Sample N random subsets of training data (with replacement)
2. Train one tree on each subset
3. Final prediction = average of all trees' predictions

**Strengths:**
- Much less overfitting than a single tree
- Handles non-linear relationships
- Built-in feature importance
- Robust to outliers

**Weaknesses:**
- Slower to train (many trees)
- Less interpretable than a single tree
- Can still overfit if trees are too deep or other regularization is too weak; adding more trees mostly increases compute cost

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=100,    # number of trees
    max_depth=10,        # limit tree depth
    random_state=42      # reproducibility
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Feature importance
importances = model.feature_importances_
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"{name}: {imp:.4f}")
```

**Watch:** [StatQuest: Random Forests](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ) (~10 min)

---

## 4. Gradient Boosting (XGBoost / LightGBM) — The Workhorse

Gradient Boosting also builds many trees, but **sequentially** instead of independently:

1. Train a small tree on the data
2. Compute the errors (residuals)
3. Train the next tree to predict those errors
4. Add the new tree's predictions to the existing ones
5. Repeat

Each tree corrects the mistakes of all previous trees. The result is a powerful model that learns complex patterns incrementally.

**XGBoost** and **LightGBM** are optimised implementations of this idea. They're the dominant models in tabular ML competitions (Kaggle) and quant finance.

**Strengths:**
- Often the best-performing model for tabular data
- Handles non-linear patterns, interactions, missing values
- Feature importance built in
- Highly tuneable

**Weaknesses:**
- Easy to overfit if hyperparameters aren't controlled
- Slower to tune (many hyperparameters)
- Less interpretable than linear regression

```python
from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=200,      # number of boosting rounds
    max_depth=4,           # keep trees shallow
    learning_rate=0.05,    # how much each tree contributes
    subsample=0.8,         # use 80% of data per tree
    random_state=42
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

```python
# LightGBM alternative (often faster)
from lightgbm import LGBMRegressor

model = LGBMRegressor(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    random_state=42,
    verbosity=-1
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

**Watch:** [StatQuest: XGBoost](https://www.youtube.com/watch?v=OtD8wVaFm6E) (~26 min — worth every minute)

---

## Time-Series Train/Test Split

**This is the most important concept in this phase. Get this wrong and your entire model is invalid.**

In regular ML, you can randomly shuffle data and split 80/20. **In time series, you cannot.** If you randomly split, your training set will contain data from 2023 and your test set will contain data from 2021. The model would be using the future to predict the past.

**Correct split: always respect time order.**

```
Timeline: ──────────────────────────────────────────────►

           │◄──── Training Data ────►│◄── Test Data ──►│
           Jan 2020                   Jan 2023         Dec 2024

The model trains on the past and is tested on the future.
Never the reverse.
```

```python
# CORRECT: time-ordered split
split_date = '2023-01-01'
train = df[df['date'] < split_date]
test = df[df['date'] >= split_date]

# WRONG: random shuffle (DO NOT DO THIS)
# from sklearn.model_selection import train_test_split
# train, test = train_test_split(df, test_size=0.2, shuffle=True)  # ← NEVER for time series
```

**Why random shuffling is catastrophic for finance:**
- The model sees "future" data in training and learns patterns that only exist because it knows what comes next
- Your backtest looks amazing but the model is useless on truly new data
- This is a form of lookahead bias — the same concept from Week 1, now in an ML context

---

## Walk-Forward Validation

A single train/test split gives you one estimate of performance. Walk-forward validation gives you many, simulating how you'd actually use the model over time:

```
Split 1: Train [2020───2021] → Test [2022 Q1]
Split 2: Train [2020───2022 Q1] → Test [2022 Q2]
Split 3: Train [2020───2022 Q2] → Test [2022 Q3]
Split 4: Train [2020───2022 Q3] → Test [2022 Q4]
...
```

Each split uses all data up to a point for training and the next chunk for testing. The training window expands over time.

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
scores = []

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)  # R²
    scores.append(score)

print(f"Average R²: {np.mean(scores):.4f} ± {np.std(scores):.4f}")
```

This tells you not just "how good is the model" but also "how stable is the model's performance over time."

---

## Hyperparameter Tuning: What to Tune

Each model has knobs that control its complexity. Too simple = underfitting. Too complex = overfitting.

| Model | Key Hyperparameters | Rule of thumb |
|-------|-------------------|---------------|
| Linear Regression | None (or regularisation strength for Ridge/Lasso) | Use Ridge if you have many features |
| Decision Tree | `max_depth`, `min_samples_leaf` | Keep depth ≤ 5–8 |
| Random Forest | `n_estimators`, `max_depth`, `max_features` | More trees rarely hurts; limit depth |
| XGBoost/LightGBM | `n_estimators`, `max_depth`, `learning_rate`, `subsample` | Lower learning_rate + more estimators = better (but slower) |

**Simple tuning approach:**
```python
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1]
}

tscv = TimeSeriesSplit(n_splits=3)
grid = GridSearchCV(XGBRegressor(), param_grid, cv=tscv, scoring='r2')
grid.fit(X_train, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best R²: {grid.best_score_:.4f}")
```

---

## Feature Importance: What Did the Model Learn?

After training, check which features the model found most useful:

```python
import matplotlib.pyplot as plt

# For tree-based models
importances = model.feature_importances_
sorted_idx = np.argsort(importances)[-15:]  # top 15

plt.barh(range(len(sorted_idx)), importances[sorted_idx])
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel('Feature Importance')
plt.title('Top 15 Features')
plt.tight_layout()
plt.show()
```

If your top features make intuitive sense (momentum, volatility), that's a good sign. If the top feature is something random or suspicious, investigate for leakage.

---

## Model Comparison Workflow

Your workflow for the project:

1. **Start with Linear Regression** — this is your baseline. If R² = 0.01, that's your number to beat.
2. **Try Random Forest** — does it improve? By how much?
3. **Try XGBoost** — with default hyperparameters first, then tune.
4. **Compare all three** — on the SAME test set, using R².
5. **Pick the best** — but understand why it's the best. If XGBoost is only marginally better than linear regression, the signal might be mostly linear.

---

## Additional Resources

| Resource | What it covers | Time |
|----------|---------------|------|
| [Scikit-learn: Choosing the right estimator](https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html) | Visual decision flowchart | 5 min |
| [XGBoost documentation](https://xgboost.readthedocs.io/) | API reference and tutorials | Reference |
| [Kaggle: Intro to ML](https://www.kaggle.com/learn/intro-to-machine-learning) | Hands-on exercises with real data | 3 hours |
| [Kaggle: Intermediate ML](https://www.kaggle.com/learn/intermediate-machine-learning) | Pipelines, XGBoost, data leakage | 4 hours |

---

**Next:** [Project — Predict Returns →](./project/README.md)

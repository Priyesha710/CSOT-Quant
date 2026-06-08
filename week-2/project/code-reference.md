# Code Reference — Libraries for the Stock Prediction Project

This document explains every library and function used in the project workflow. If you've never used Python for data science, start here.

---

## Table of Contents

1. [pandas — Data Loading & Manipulation](#pandas)
2. [NumPy — Numerical Operations](#numpy)
3. [Matplotlib — Plotting](#matplotlib)
4. [Seaborn (sns) — Statistical Visualization](#seaborn)
5. [scikit-learn — Machine Learning](#scikit-learn)
6. [XGBoost — Gradient Boosted Trees](#xgboost)
7. [Putting It All Together](#putting-it-all-together)

---

## pandas

**What it is:** The core library for working with tabular data (think spreadsheets/CSVs in Python). Everything lives in a `DataFrame` — a 2D table with labeled rows and columns.

```python
import pandas as pd
```

### Loading Data

```python
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
```

| What it does | Details |
|---|---|
| `pd.read_csv(path)` | Reads a CSV file into a DataFrame. Each row becomes a row in the table, each column header becomes a column name. |

After loading, `train` is a DataFrame you can inspect, filter, and transform.

### Inspecting the DataFrame

```python
train.shape           # → (num_rows, num_columns) e.g. (10000, 25)
train.describe()      # → summary stats: mean, std, min, max, quartiles for each column
train.isnull().sum()  # → count of missing (NaN) values per column
train.columns         # → list of all column names
train.head()          # → first 5 rows (quick visual check)
train.dtypes          # → data type of each column (float64, int64, object, etc.)
```

### Selecting Columns

```python
# Single column → returns a Series (1D)
train['target']

# Multiple columns → returns a DataFrame (2D)
train[['target', 'id']]

# All columns EXCEPT certain ones (common pattern for separating features from target)
feature_cols = [c for c in train.columns if c not in ['target', 'id']]
X_train = train[feature_cols]
```

**Key concept:** A `Series` is a single column. A `DataFrame` is a collection of Series (the full table).

### Handling Missing Values

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)
```

| Method | What it does |
|---|---|
| `.fillna(value)` | Replaces all NaN cells with `value`. If `value` is a Series (like `.median()`), each column gets its own fill value. Useful for quick experiments, but be careful not to fit those statistics on future validation rows. |
| `.median()` | Returns the median (middle value) of each numeric column. |
| `.mean()` | Returns the mean (average) of each numeric column. |
| `.dropna()` | Removes rows that contain any NaN (alternative to filling). |

### Creating DataFrames

```python
submission = pd.DataFrame({
    'id': test['id'],
    'predicted_target': predictions
})
submission.to_csv('my_submission.csv', index=False)
```

| What | Details |
|---|---|
| `pd.DataFrame({...})` | Creates a new DataFrame from a dictionary. Keys become column names, values become column data. |
| `.to_csv(path, index=False)` | Saves to CSV. `index=False` prevents pandas from writing row numbers as an extra column. |

### Useful Operations You'll Need

```python
# Correlation between all features and target
train[feature_cols + ['target']].corr()['target'].sort_values()

# Value counts (for categorical columns)
train['some_col'].value_counts()

# Filter rows
train[train['target'] > 0]          # only positive returns
train[train['target'].abs() < 0.1]  # remove extreme outliers

# Apply a function to a column
train['target_clipped'] = train['target'].clip(-0.05, 0.05)  # cap at ±5%

# iloc — select by position
train.iloc[0:100]         # first 100 rows
train.iloc[train_idx]     # rows at specific integer positions (used in cross-validation)
```

---

## NumPy

**What it is:** The foundation for numerical computing. Provides fast arrays and math operations. pandas is built on top of NumPy.

```python
import numpy as np
```

### When You'll Use It

```python
# Create arrays
np.array([1, 2, 3, 4, 5])

# Math operations (element-wise, vectorized — fast)
np.mean(values)
np.std(values)
np.sqrt(values)
np.log(values)        # natural log
np.abs(values)        # absolute value

# NaN-safe versions (ignore NaN instead of returning NaN)
np.nanmean(values)
np.nanstd(values)

# Useful constants
np.nan    # "Not a Number" — represents missing data
np.inf    # infinity
```

### Common Patterns in This Project

```python
# Clip extreme values (cap outliers)
y_train_clipped = np.clip(y_train, -0.05, 0.05)

# Check for infinity or NaN in predictions (must be clean before submission)
np.isinf(predictions).any()   # → True/False
np.isnan(predictions).any()   # → True/False

# Replace inf with NaN, then fill
predictions = np.where(np.isinf(predictions), 0, predictions)

# Standard scaling (z-score normalization)
mean = np.mean(X_train, axis=0)
std = np.std(X_train, axis=0)
X_scaled = (X_train - mean) / std
```

**Key concept:** NumPy operations are *vectorized* — they operate on entire arrays at once without Python loops, making them 10–100x faster than looping row by row.

---

## Matplotlib

**What it is:** The base plotting library. Everything you see in a chart (axes, labels, titles) ultimately goes through matplotlib.

```python
import matplotlib.pyplot as plt
```

### Basic Plots

```python
# Histogram — see distribution of a single variable
train['target'].hist(bins=50)
plt.title('Target Distribution')
plt.xlabel('Return')
plt.ylabel('Frequency')
plt.show()

# Line plot
plt.plot(values)
plt.show()

# Scatter plot — relationship between two variables
plt.scatter(train['feature_1'], train['target'], alpha=0.3)
plt.xlabel('Feature 1')
plt.ylabel('Target')
plt.show()
```

| Function | What it does |
|---|---|
| `.hist(bins=50)` | Draws a histogram. `bins` = number of bars (more bins = more detail). |
| `plt.title(...)` | Sets the chart title. |
| `plt.xlabel(...)` / `plt.ylabel(...)` | Labels for x/y axes. |
| `plt.show()` | Renders and displays the plot. Always call at the end. |
| `plt.figure(figsize=(12, 6))` | Create a new figure with custom size (width, height in inches). |
| `plt.savefig('plot.png')` | Save plot to file instead of displaying. |

### Multiple Subplots

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(train['target'], bins=50)
axes[0].set_title('Target Distribution')
axes[1].scatter(train['feature_1'], train['target'], alpha=0.1)
axes[1].set_title('Feature 1 vs Target')
plt.tight_layout()
plt.show()
```

---

## Seaborn

**What it is:** Built on matplotlib. Makes statistical plots with less code and better aesthetics. Imported as `sns` (named after a fictional character).

```python
import seaborn as sns
```

### Plots You'll Use for EDA (Exploratory Data Analysis)

```python
# Correlation heatmap — shows which features relate to each other
corr_matrix = train[feature_cols + ['target']].corr()
plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, cmap='coolwarm', center=0, annot=False)
plt.title('Feature Correlation Matrix')
plt.show()
```

| Parameter | Meaning |
|---|---|
| `cmap='coolwarm'` | Color scheme: blue for negative correlation, red for positive. |
| `center=0` | 0 correlation = neutral color. |
| `annot=True` | Print correlation values in each cell (gets crowded with many features). |

```python
# Distribution plot — histogram + density curve
sns.histplot(train['target'], bins=50, kde=True)
plt.show()

# Box plot — shows median, quartiles, and outliers
sns.boxplot(x=train['target'])
plt.show()

# Pair plot — scatter plots for all pairs of selected features (slow with many columns)
sns.pairplot(train[['feature_1', 'feature_2', 'feature_3', 'target']])
plt.show()

# Regression plot — scatter with best-fit line
sns.regplot(x='feature_1', y='target', data=train, scatter_kws={'alpha': 0.1})
plt.show()
```

**When to use seaborn vs matplotlib:** Use seaborn when you want a statistical summary (heatmap, boxplot, distributions). Use raw matplotlib when you need custom control (annotations, unusual layouts).

---

## scikit-learn

**What it is:** The standard ML library for Python. Provides models, preprocessing, cross-validation, and metrics — all with a consistent API.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import TimeSeriesSplit
```

### The Universal API Pattern

Every model in scikit-learn follows the same pattern:

```python
model = SomeModel(hyperparameters)   # 1. Create the model
model.fit(X_train, y_train)          # 2. Train it on data
predictions = model.predict(X_test)  # 3. Make predictions
```

This is the same whether you're using LinearRegression, Ridge, RandomForest, or any other model. Learn this pattern once, use it everywhere.

### Linear Regression (Baseline Model)

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Fits a straight line (hyperplane in multiple dimensions) through the data. No hyperparameters to tune. Fast. Often your first model to establish a baseline score.

### Ridge Regression (Regularized Linear)

```python
from sklearn.linear_model import Ridge

model = Ridge(alpha=1.0)  # alpha controls regularization strength
model.fit(X_train, y_train)
```

Like LinearRegression but penalizes large coefficients. Prevents overfitting when you have many features. Higher `alpha` = more penalty = simpler model.

### Metrics — R² Score

```python
from sklearn.metrics import r2_score

score = r2_score(y_true, y_predicted)
```

| Score | Meaning |
|---|---|
| 1.0 | Perfect predictions |
| 0.0 | Same as predicting the mean every time |
| < 0 | Worse than the mean — something is wrong |
| 0.01–0.05 | Good for financial data (returns are inherently noisy) |

### Cross-Validation — TimeSeriesSplit

```python
from sklearn.impute import SimpleImputer
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline

model = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('regressor', LinearRegression())
])

tscv = TimeSeriesSplit(n_splits=5)

for train_idx, val_idx in tscv.split(X_train):
    # train_idx and val_idx are arrays of row indices
    model.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
    val_pred = model.predict(X_train.iloc[val_idx])
    score = r2_score(y_train.iloc[val_idx], val_pred)
    print(f"Fold R²: {score:.4f}")
```

Using a `Pipeline` keeps the imputer inside each fold. That avoids leaking future information from the validation period into the fill values.

**Why TimeSeriesSplit instead of random split?**

With time-series data, you must train on the *past* and validate on the *future*. Random shuffling leaks future information into training — your model looks good in validation but fails on new data.

TimeSeriesSplit with 5 splits creates:
```
Fold 1: Train=[0..199],    Val=[200..399]
Fold 2: Train=[0..399],    Val=[400..599]
Fold 3: Train=[0..599],    Val=[600..799]
Fold 4: Train=[0..799],    Val=[800..999]
Fold 5: Train=[0..999],    Val=[1000..1199]
```

Each fold, the training window grows and the validation window is always in the future.

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# GridSearchCV — tries ALL combinations (exhaustive but slow)
param_grid = {
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 500]
}
grid_search = GridSearchCV(
    estimator=XGBRegressor(),
    param_grid=param_grid,
    cv=TimeSeriesSplit(n_splits=3),
    scoring='r2',
    verbose=1
)
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)
best_model = grid_search.best_estimator_

# RandomizedSearchCV — samples random combinations (faster for large search spaces)
from scipy.stats import uniform, randint
param_distributions = {
    'max_depth': randint(3, 8),
    'learning_rate': uniform(0.01, 0.2),
    'n_estimators': [100, 200, 300, 500]
}
random_search = RandomizedSearchCV(
    estimator=XGBRegressor(),
    param_distributions=param_distributions,
    n_iter=20,  # try 20 random combinations
    cv=TimeSeriesSplit(n_splits=3),
    scoring='r2',
    verbose=1
)
random_search.fit(X_train, y_train)
```

### Feature Importance (after training)

```python
# For tree-based models (RandomForest, XGBoost, etc.)
importances = model.feature_importances_
feature_importance = pd.Series(importances, index=feature_cols).sort_values(ascending=False)
feature_importance.head(20).plot(kind='barh')
plt.title('Top 20 Features')
plt.show()

# For linear models
coefficients = pd.Series(model.coef_, index=feature_cols).sort_values()
```

### Preprocessing (Optional but Useful)

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # computes mean/std AND transforms
X_test_scaled = scaler.transform(X_test)          # uses TRAIN mean/std (no data leakage)
```

`StandardScaler` converts each feature to have mean=0, std=1. Linear models and neural networks benefit from this. Tree models (XGBoost, RandomForest) don't need it.

---

## XGBoost

**What it is:** An optimized gradient boosting library. Builds many small decision trees sequentially, each one correcting the errors of the previous ones. Usually the top performer for tabular data.

```python
from xgboost import XGBRegressor
```

### Basic Usage

```python
model = XGBRegressor(
    n_estimators=200,     # number of trees to build
    max_depth=4,          # max depth of each tree (controls complexity)
    learning_rate=0.05    # shrinkage — how much each tree contributes
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### Key Hyperparameters

| Parameter | What it controls | Good starting values | Guidance |
|---|---|---|---|
| `n_estimators` | Number of trees | 100–500 | More trees = slower + risk of overfitting (but less with low learning_rate) |
| `max_depth` | Tree complexity | 3–6 | Lower = simpler/faster. Higher = captures more patterns but overfits |
| `learning_rate` | Step size per tree | 0.01–0.1 | Lower = needs more trees but usually better final score |
| `subsample` | Fraction of rows per tree | 0.7–0.9 | Random sampling reduces overfitting |
| `colsample_bytree` | Fraction of features per tree | 0.7–0.9 | Like subsample but for columns |
| `reg_alpha` | L1 regularization | 0–1 | Pushes unimportant feature weights to exactly 0 |
| `reg_lambda` | L2 regularization | 1–5 | Penalizes large weights, prevents overfitting |

### Practical Tips

```python
# Handle NaN natively (XGBoost can learn which direction to send NaN values)
# So you can skip fillna() for XGBoost specifically, but filling is still safer

# Early stopping — stop training when validation score stops improving
model = XGBRegressor(n_estimators=1000, learning_rate=0.05, max_depth=4)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],     # validation set to monitor
    verbose=50                      # print score every 50 trees
)

# Feature importance
model.feature_importances_   # array of importance scores (higher = more useful)
```

### XGBoost vs Linear Regression — When to Use Which

| Situation | Better model |
|---|---|
| Linear relationships, few features | LinearRegression / Ridge |
| Non-linear patterns, feature interactions | XGBoost |
| Very small dataset (<500 rows) | LinearRegression (less overfitting risk) |
| Large dataset, many features | XGBoost |
| Need interpretability | LinearRegression (coefficients are direct) |
| Need best raw performance | XGBoost (usually) |

---

## Putting It All Together

Here's the complete workflow using all libraries, annotated for a beginner:

```python
# === 1. IMPORTS ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor

# === 2. LOAD DATA ===
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

# === 3. EXPLORE ===
print(f"Train shape: {train.shape}")
print(f"Missing values:\n{train.isnull().sum()[train.isnull().sum() > 0]}")

sns.histplot(train['target'], bins=50, kde=True)
plt.title('Target Distribution')
plt.show()

# === 4. PREPARE FEATURES ===
feature_cols = [c for c in train.columns if c not in ['target', 'id']]
X_train = train[feature_cols].fillna(train[feature_cols].median())
y_train = train['target']
X_test = test[feature_cols].fillna(train[feature_cols].median())

# === 5. CROSS-VALIDATE ===
tscv = TimeSeriesSplit(n_splits=5)
models = {
    'Ridge': Ridge(alpha=1.0),
    'XGBoost': XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.05)
}

for name, model in models.items():
    scores = []
    for train_idx, val_idx in tscv.split(X_train):
        model.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
        pred = model.predict(X_train.iloc[val_idx])
        scores.append(r2_score(y_train.iloc[val_idx], pred))
    print(f"{name}: mean R² = {np.mean(scores):.4f} (±{np.std(scores):.4f})")

# === 6. TRAIN FINAL MODEL & PREDICT ===
final_model = XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.05)
final_model.fit(X_train, y_train)
predictions = final_model.predict(X_test)

# === 7. SUBMIT ===
submission = pd.DataFrame({'id': test['id'], 'predicted_target': predictions})
submission.to_csv('my_submission.csv', index=False)
print("Done. Saved my_submission.csv")
```

---

## Quick Glossary

| Term | Meaning |
|---|---|
| **DataFrame** | A 2D table (rows × columns) in pandas |
| **Series** | A single column from a DataFrame |
| **NaN** | "Not a Number" — represents missing data |
| **Fit** | Train a model on data (learn patterns) |
| **Predict** | Use the trained model to generate outputs for new data |
| **Hyperparameter** | A setting you choose before training (not learned from data) |
| **Overfitting** | Model memorises training data and fails on new data |
| **Cross-validation** | Splitting training data into folds to estimate real-world performance |
| **R²** | Score from -∞ to 1. Higher = better predictions. 0 = same as predicting the average. |
| **Feature** | An input column used to make predictions |
| **Target** | The column you're trying to predict |
| **Regularization** | Penalty on model complexity to prevent overfitting |
| **Gradient boosting** | Building many small models sequentially, each fixing previous errors |
| **EDA** | Exploratory Data Analysis — looking at the data before modelling |

---

## Installing These Libraries

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost
```

Or with conda:
```bash
conda install pandas numpy matplotlib seaborn scikit-learn xgboost
```

All of these come pre-installed in Google Colab and most Jupyter environments.

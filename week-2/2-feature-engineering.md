# Phase 2: Feature Engineering — Turning Prices Into Predictions

*~3 hours | The most important phase for your project score*

---

## Why Features Matter More Than Models

Here's a truth that surprises most beginners: **the features you build matter far more than which model you choose.** A simple linear regression with great features will beat XGBoost with bad features every time.

A model can only learn patterns that exist in its inputs. If your features don't contain information about future returns, no model — no matter how complex — can extract predictions from them.

Feature engineering is where domain knowledge (what you learned in Week 1 about markets) meets machine learning.

---

## Why Raw Price Is Not a Feature

You might think: "just give the model today's closing price and let it predict tomorrow's return." This fails for fundamental reasons:

1. **Non-stationarity.** A stock at ₹500 today and ₹5000 a year from now has completely different price levels, but the return dynamics might be identical. The model has no way to learn this if you feed it raw prices.

   *What does "stationary" mean?* A time series is **stationary** if its statistical properties — mean, variance, autocorrelation — don't change over time. Stock prices are non-stationary (they trend upward over decades, and volatility changes across regimes). Returns, on the other hand, tend to fluctuate around a stable mean with roughly constant variance — making them much closer to stationary, and therefore usable as ML inputs.

2. **Scale dependence.** If you train on multiple stocks, one trading at ₹50 and another at ₹5000, raw price creates a false distinction that has nothing to do with returns.

3. **Trend contamination.** Raw price contains the long-term trend. Your model will "predict" that prices go up because they've historically trended up — that's not a useful signal.

**The fix:** Transform prices into stationary, scale-independent quantities. Returns, ratios, z-scores, percentile ranks.

> **Z-score** = how many standard deviations a value is from its mean: `z = (x - mean) / std`. A z-score of +2 means the value is 2 standard deviations above the mean. This lets you compare across different stocks and time periods on the same scale.
>
> **Percentile rank** = what fraction of historical values fall below the current value. If today's RSI is at the 90th percentile, it means RSI was lower than this 90% of the time. Useful when the raw value's scale is hard to interpret.

---

## Returns: Your Base Transformation

Everything starts from returns:

```python
# Percentage return
pct_return = (price_today - price_yesterday) / price_yesterday

# Log return (preferred — additive over time)
log_return = np.log(price_today / price_yesterday)
```

Log returns are preferred because:
- They're additive: multi-day return = sum of daily log returns
- They're approximately symmetric for small returns
- They're closer to normally distributed

---

## Pandas Methods You'll Use Everywhere

Before diving into features, here are three pandas methods that appear in almost every feature formula. Understanding them is essential:

| Method | What it does | Example |
|--------|-------------|---------|
| `.diff()` | Subtracts the previous row's value from the current row | `df['Close'].diff()` → today's price minus yesterday's price |
| `.shift(n)` | Moves data forward or backward by `n` rows. `shift(1)` gives you yesterday's value on today's row | `df['Close'].shift(1)` → yesterday's close, aligned to today |
| `.rolling(n)` | Creates a sliding window of `n` rows, then you chain an aggregation (`.mean()`, `.std()`, etc.) | `df['Close'].rolling(20).mean()` → average of last 20 closes |

```python
# .diff() — price change from yesterday
df['price_change'] = df['Close'].diff()     # Close_today - Close_yesterday

# .shift() — access previous values
df['prev_close'] = df['Close'].shift(1)     # yesterday's close on today's row
df['prev_close_5'] = df['Close'].shift(5)   # close from 5 days ago

# .rolling() — windowed computations
df['sma_10'] = df['Close'].rolling(10).mean()   # 10-day simple moving average
df['vol_10'] = df['log_return'].rolling(10).std()  # 10-day rolling volatility
```

> **Note:** `.rolling(n)` produces `NaN` for the first `n-1` rows (not enough data to fill the window). `.shift(n)` produces `NaN` for the first `n` rows. `.diff()` produces `NaN` for the first row. This is expected — we handle it later in the "Handling Missing Values" section.

---

## Categories of Useful Features

### 1. Rolling Statistics

Compute stats over a sliding window of N days:

| Feature | Formula | Intuition |
|---------|---------|-----------|
| SMA_20 | Mean of last 20 closing prices | Smoothed trend level |
| Rolling Std (20d) | Std dev of last 20 returns | Recent volatility |
| Rolling Min/Max | Min/max price in last N days | Recent range |
| Price vs SMA | (Close - SMA_20) / SMA_20 | How far price deviates from trend |

```python
df['sma_20'] = df['Close'].rolling(20).mean()
df['volatility_20'] = df['log_return'].rolling(20).std()
df['price_vs_sma'] = (df['Close'] - df['sma_20']) / df['sma_20']
```

### 2. Momentum Indicators

Measure the speed and direction of price movement.

**SMA vs EMA:** You already know SMA (Simple Moving Average) — it weights all days equally. An **EMA (Exponential Moving Average)** gives more weight to recent days and less to older ones, so it reacts faster to price changes. An EMA with span 12 means the most recent day has the highest weight, and the influence of each older day decays exponentially. In pandas: `df['Close'].ewm(span=12).mean()`.

| Feature | What it captures |
|---------|-----------------|
| **RSI (14)** | Relative Strength Index — overbought/oversold on 0–100 scale |
| **MACD** | Difference between 12-day EMA and 26-day EMA — trend momentum |
| **Rate of Change (N)** | Percentage change over N days |
| **Return Momentum** | Sum of returns over last N days |

```python
# RSI (simplified)
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
df['rsi_14'] = 100 - (100 / (1 + rs))

# Rate of change
df['roc_10'] = df['Close'].pct_change(10)
```

**Read:** [Investopedia: RSI](https://www.investopedia.com/terms/r/rsi.asp) | [Investopedia: MACD](https://www.investopedia.com/terms/m/macd.asp)

### 3. Volume Features

Price alone doesn't tell the whole story. Volume confirms conviction:

| Feature | Intuition |
|---------|-----------|
| Volume MA ratio | Current volume / 20-day avg volume — is today unusual? |
| Volume spike | Binary: is volume > 2× its 20-day mean? |
| Price-volume divergence | Price up + volume down = weak move |

```python
df['volume_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
df['volume_spike'] = (df['volume_ratio'] > 2.0).astype(int)
```

### 4. Lag Features

What happened recently often has predictive power for what happens next:

| Feature | Intuition |
|---------|-----------|
| Return yesterday | Short-term autocorrelation (or mean reversion) |
| Return 5 days ago | Weekly momentum |
| Return 20 days ago | Monthly momentum |
| Cumulative return (5d) | Recent trend direction and magnitude |

```python
df['return_lag_1'] = df['log_return'].shift(1)
df['return_lag_5'] = df['log_return'].shift(5)
df['cum_return_5d'] = df['log_return'].rolling(5).sum()
```

### 5. Volatility Features

How much the asset has been moving — and whether that's changing:

| Feature | Intuition |
|---------|-----------|
| Realised vol (5d vs 20d) | Is short-term vol higher than usual? |
| Vol ratio | Short-term vol / long-term vol — regime detection |
| ATR (Average True Range) | Range-based volatility measure |

```python
df['vol_5'] = df['log_return'].rolling(5).std()
df['vol_20'] = df['log_return'].rolling(20).std()
df['vol_ratio'] = df['vol_5'] / df['vol_20']
```

---

## The Critical Rule: No Future Leakage

> **A feature computed on day T must use ONLY data from day T and before. Never from day T+1 or later.**

This sounds obvious but is shockingly easy to violate:

**Leakage examples:**
- Using today's return to predict today's return (circular)
- Computing a moving average that includes future prices (wrong window alignment)
- Normalising features using statistics computed over the full dataset (including test period)
- Using the target column as a feature (instant "perfect" predictions that fail on new data)

**How to check:** After engineering features, look at each one and ask: "On day T, would I have had access to all the data used to compute this feature?" If the answer is no for even one row, you have leakage.

**The consequence of leakage:** Your model will appear to work beautifully in backtesting and fail completely on new data. This is the single most common reason ML models "work" in research and die in production.

---

## Feature-Target Correlation: A Quick Sanity Check

Before training a model, check if your features actually correlate with the target:

```python
correlations = df[feature_columns + ['target']].corr()['target'].drop('target')
print(correlations.sort_values(ascending=False))
```

> A feature doesn't need very high correlation to be useful. ML models find non-linear combinations that individual correlations don't reveal. But zero-correlation features across the board means you need better features.

### The Correlation Matrix

The single-column check above shows each feature's correlation with the target. But features also correlate **with each other** — and that matters. If two features carry nearly identical information (e.g. SMA_20 and SMA_25), adding both doesn't help the model and can hurt interpretability.

A **correlation matrix** shows the pairwise correlation between *every* pair of columns. It's a square table where row *i*, column *j* contains the Pearson correlation between feature *i* and feature *j*. The diagonal is always 1.0 (every feature is perfectly correlated with itself).

```python
feature_cols = ['rsi_14', 'volatility_20', 'price_vs_sma', 'roc_10',
                'volume_ratio', 'return_lag_1', 'vol_ratio']
corr_matrix = df[feature_cols].corr()
print(corr_matrix)
```

### Visualising with a Heatmap

A raw correlation matrix of 10+ features is hard to read as a table of numbers. A **heatmap** turns it into a colour-coded grid — dark red for strong positive correlation, dark blue for strong negative, white/pale for near-zero.

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, square=True)
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.show()
```

**How to read the heatmap:**

| What you see | What it means | Action |
|-------------|---------------|--------|
| Two features with correlation > 0.85 | They carry nearly the same information | Consider dropping one |
| Feature-target correlation > 0.3 |  Strong for financial data | Good — this is what you want |
| A block of highly correlated features | They're all measuring the same thing | Pick the best one or combine into a single composite feature |
| Most cells near 0 | Features capture diverse, independent signals | Good — this is what you want |

> **Rule of thumb:** If two features have |correlation| > 0.85, they're redundant. Keep the one with higher target correlation, or the one that's easier to interpret.

---

## Handling Missing Values

Rolling computations produce NaN for the first N rows (not enough history). You must handle these before training:

```python
# Option 1: Drop rows with NaN (simplest, lose some data)
df = df.dropna()

# Option 2: Forward-fill (risky — can introduce leakage if not careful)
df = df.fillna(method='ffill')

# Option 3: Fill with column median (safe for tree-based models)
df = df.fillna(df.median())
```

For your project: dropping NaN rows is the safest and simplest approach. You'll lose the first ~20 rows (depending on your longest rolling window) which is fine with years of daily data.

---

## Additional Resources

| Resource | What it covers | Time |
|----------|---------------|------|
| [Investopedia: Technical Indicators](https://www.investopedia.com/terms/t/technicalindicator.asp) | Overview of all common indicators | 30 min |
| [TA-Lib Python docs](https://ta-lib.github.io/ta-lib-python/) | Library reference (not required, just useful) | Reference |
| [YouTube: Feature Engineering for Time Series](https://www.youtube.com/watch?v=9QtL7m3YS9I) | Visual walkthrough | 20 min |

---

**Next:** [Phase 3 — ML Models →](3-models.md)

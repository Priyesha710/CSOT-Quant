# Phase 1: Machine Learning Foundations

*~2 hours | Read and watch in order*

---

## What is Machine Learning?

In Week 1, you wrote a signal by hand: "when the 20-day MA crosses above the 60-day MA, go long." You decided the rule. You decided the threshold.

Machine learning flips this: **you provide data and a target, and the algorithm finds the rules.** Instead of you saying "this pattern predicts returns," the model discovers which patterns in the data are associated with higher or lower future returns.

This is powerful when:
- There are too many potential patterns to test by hand
- Interactions between features are complex (momentum + volatility + volume together)
- You want to combine many weak signals into one stronger prediction

This is dangerous when:
- You have too little data relative to the complexity of your model
- The patterns in your data are noise, not signal
- You don't understand what the model learned

**Watch:** [StatQuest: Machine Learning Fundamentals](https://www.youtube.com/watch?v=Gv9_4yMHFhI) (~10 min, visual and beginner-friendly)

---

## Supervised Learning

The type of ML we'll use is **supervised learning**. The setup:

- You have a dataset of **examples** (rows)
- Each example has **features** (input columns) and a **target** (what you want to predict)
- The model learns a function: `features → target`
- Once trained, you give it new features (without the target) and it produces a prediction

In our case:
- **Features:** things derived from historical prices — moving averages, RSI, volatility, lag returns, etc.
- **Target:** the actual return over the next N days

The model tries to learn: "when these feature values look like *this*, the return tends to be *that*."

---

## Regression vs Classification

Two flavours of supervised learning:

| | Regression | Classification |
|---|---|---|
| **Predicts** | A continuous number | A category/label |
| **Example** | "Return will be +0.3%" | "Price will go UP" |
| **Output** | Any real number | One of a fixed set of classes |
| **Metrics** | R², RMSE, MAE | Accuracy, precision, recall |

**We're doing regression** — predicting the actual magnitude of returns, not just direction. This is harder but more informative. If you know the magnitude, you also know the direction (positive = up, negative = down).

---

## Train and Test: Why You Split Your Data

Imagine you memorise the answers to a practice exam. You'll score 100% on that exact exam — but on the real one, you'll fail. ML models can do the same thing.

**Training data** is what the model learns from. **Test data** is the unseen exam — data the model has never seen, used to measure how well it generalises.

```
┌─────────────────────────────────────────────────┐
│              Your Full Dataset                   │
├────────────────────────────────┬────────────────┤
│         Training Set           │   Test Set     │
│    (model learns from this)    │  (evaluate on  │
│                                │   this only)   │
└────────────────────────────────┴────────────────┘
```

Rules:
- The model NEVER sees the test set during training
- You evaluate performance ONLY on the test set
- A model that does well on training but poorly on test has **overfit**

> If you only measure performance on training data, you're measuring memorisation, not learning.

---

## Overfitting: The Core Enemy

**Overfitting** = your model learned the noise in the training data rather than the actual signal.

Signs of overfitting:
- Great performance on training data, poor performance on test data
- Model is very complex (many parameters) relative to the amount of data
- Performance improves on training set but degrades on test set as you add complexity

**Why this matters for finance:** Markets are extremely noisy. A model can easily find "patterns" in historical data that are pure coincidence. If your model has R² = 0.9 on training data but R² = -0.1 on test data, it memorised noise.

**Intuition:** A simple model that captures a real pattern will generalise. A complex model that perfectly fits training data has probably memorised randomness.

**Watch:** [StatQuest: Bias and Variance](https://www.youtube.com/watch?v=EuBBz3bI-aA) (~7 min)

**Read:** [Overfitting vs Underfitting — Towards Data Science](https://towardsdatascience.com/overfitting-versus-underfitting/)

---

## R-Squared (R²): How We Score Predictions

R-squared measures how much better your model is compared to simply predicting the mean every time.

**Formula (conceptual):**
```
R² = 1 - (sum of squared prediction errors) / (sum of squared deviations from the mean)
```

**What the values mean:**

| R² value | Interpretation |
|----------|---------------|
| 1.0 | Perfect predictions (suspicious in finance) |
| 0.5 | Model explains 50% of the variance in returns |
| 0.0 | Model is no better than predicting the mean |
| Negative | Model is WORSE than just predicting the mean |

In real financial return predictions, even R² = 0.02–0.05 can be economically significant at scale. R² = 0.8 would mean markets are almost perfectly predictable (they're not).

**Watch:** [StatQuest: R-squared, clearly explained](https://www.youtube.com/watch?v=bMccdk8EdGo) (~12 min)

---

## Putting It Together: The ML Workflow

```
Raw Data → Feature Engineering → Train/Test Split → Model Training → Evaluation → Prediction
```

1. Start with raw price/volume data
2. Engineer features (Phase 2)
3. Split into train and test sets (respecting time order!)
4. Train a model on the training set
5. Evaluate on the test set using R²
6. If performance is bad: try different features, different model, or simplify
7. Once satisfied: predict on the final unseen test set

---

## Additional Resources

| Resource | What it covers | Time |
|----------|---------------|------|
| [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course) | Full intro to ML, interactive | 2–3 hours |
| [3Blue1Brown: Neural Networks](https://www.youtube.com/watch?v=aircAruvnKk) | Visual intuition for how models learn (optional) | 20 min |
| [Kaggle: Intro to ML](https://www.kaggle.com/learn/intro-to-machine-learning) | Hands-on mini-course with exercises | 3 hours |

---

**Next:** [Phase 2 — Feature Engineering →](2-feature-engineering.md)

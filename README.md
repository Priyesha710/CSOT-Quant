# 📈 CSOT Quant Finance & Research — Week 1
**Markets through a programmer's lens.**

This week has three phases. Work through them in order — each one feeds the next. Total time is ~8–10 hours; you have the full week to finish.

---

## Phase 1: Build the Mental Model
*~3.5 hours — do this before anything else*

Most people arrive here having heard the word "quant" and imagining either a black box that prints money or a wall of incomprehensible math. Neither is accurate. Phase 1 is about replacing that picture with a correct one: what the actual workflow looks like, what the fundamental quantities are, and why the math is set up the way it is.

Don't rush this. The rest of the week assumes you have these ideas loaded.

---

**What quant trading actually is**

**1. "What is Quantitative Trading?" — Investopedia**
Start here. Get the vocabulary straight: signal, alpha, systematic vs. discretionary. Everything this week uses this language.
https://www.investopedia.com/terms/q/quantitative-trading.asp
*15 min*

**2. "The Basics of Algorithmic Trading" — Investopedia**
One distinction worth making early: algorithmic execution (automating a decision a human already made) versus quantitative strategy (using data to make the decision in the first place). We're doing the second one.
https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp
*20 min*

**Video 1: "How Renaissance Technologies Made 66% Returns for 30 Years" — Patrick Boyle (YouTube)**
Watch it not for inspiration, but as a case study in process: find a pattern, test it without fooling yourself, manage the risk, repeat. The returns are the output. The process is what's worth understanding.
https://www.youtube.com/watch?v=dARMFwMGFnI
*25 min*

---

**The math you'll use constantly**

**3. "Rate of Return: Definition, Formula, and Example" — Investopedia**
Simple returns versus log returns. The reason practitioners prefer log returns isn't aesthetic — the additive property over time makes the mathematics tractable.
https://www.investopedia.com/terms/r/rateofreturn.asp
*15 min*

**4. "Volatility: Meaning in Finance and How It Works With Stocks" — Investopedia**
Volatility is a precise quantity: the standard deviation of returns. It determines position sizing, it shows up in every performance metric, and it's how you tell whether a pattern in the data might be real or might just be noise. Read the historical vs. implied section carefully.
https://www.investopedia.com/terms/v/volatility.asp
*15 min*

**5. "Normal Distribution in Finance" — Corporate Finance Institute**
Most introductory quant material assumes returns are normally distributed. This explains what that assumption buys you — and exactly where it breaks. Knowing *why* an assumption is wrong is more useful than believing it's right.
https://corporatefinanceinstitute.com/resources/excel/normal-distribution/
*15 min*

**Video 2: "Statistics for Trading — Mean, Variance, and Returns Explained" — Quantra (YouTube)**
Applied, not theoretical. Shows you the numbers and what they mean in context.
https://www.youtube.com/watch?v=1DS7hb3hAlY
*20 min*

---

**Before moving to Phase 2, answer these two questions in writing:**

- In two or three sentences: what separates a quant strategy from a trading opinion?
- Pick any stock you're familiar with. Without looking at any data: what do you expect its average daily return to be? Do you expect the return distribution to be symmetric? Name one event in the last five years that should show up as a clear outlier. You'll check your intuitions in the task.

---

## Phase 2: Signals, Backtesting, and Measuring What Matters
*~3.5 hours*

Phase 2 is the intellectual core of the week. You'll learn what a signal is, how you go from an observation to a testable hypothesis, how to evaluate whether a strategy actually worked, and — critically — how not to fool yourself with the results.

These ideas are inseparable. Read them together before you write any code.

---

**From observation to hypothesis**

**6. "What is a Trading Signal?" — Investopedia**
What a signal is, how entry and exit rules get defined from one, and what makes a signal precise enough to implement.
https://www.investopedia.com/terms/t/trade-signal.asp
*15 min*

**7. "Moving Averages: A Practical Guide" — Investopedia**
The simplest non-trivial signal in existence, and a good lesson in why simple signals look compelling on a historical chart and often disappoint in practice. Read it to understand the structure of a momentum signal, not to copy the strategy.
https://www.investopedia.com/terms/m/movingaverage.asp
*20 min*

**8. "The Efficient Market Hypothesis" — Investopedia**
If markets were perfectly efficient, no signal would work. If they were perfectly inefficient, this would be easy. Neither is true. Understanding where the edge might actually exist sets the right level of ambition.
https://www.investopedia.com/terms/e/efficientmarkethypothesis.asp
*15 min*

**Video 3: "How to Build a Trading Strategy Step by Step" — Algo Trading 101 (YouTube)**
The pipeline from idea to signal to rules to backtest, and why forming a hypothesis before touching data is the discipline that makes results meaningful.
https://www.youtube.com/watch?v=9Y3yaoi9rUQ
*20 min*

---

**Reading a backtest without fooling yourself**

**9. "The Basics of Backtesting" — Investopedia**
Definitions, standard metrics, and the assumptions baked into every backtest. The limitations section is the most important part of the page.
https://www.investopedia.com/terms/b/backtesting.asp
*20 min*

**10. "Sharpe Ratio: Definition, Formula, and What It Measures" — Investopedia**
The most widely used performance metric in quant finance. It answers one question: how much return are you getting per unit of risk taken? Read this carefully — you'll compute it in the task and every week after.
https://www.investopedia.com/terms/s/sharperatio.asp
*15 min*

**11. "Maximum Drawdown (MDD): Definition, Calculation, and Use" — Investopedia**
Sharpe tells you about the average experience. Drawdown tells you about the worst stretch — the peak-to-trough loss you'd have had to sit through without quitting. A strategy with Sharpe 2.0 and a 70% drawdown is not a strategy most people can actually run. Both numbers matter.
https://www.investopedia.com/terms/m/maximum-drawdown.asp
*15 min*

**12. "Sortino Ratio: Definition, Formula, Calculation, and Example" — Investopedia**
A variation on Sharpe that only penalises downside volatility. Read it alongside the Sharpe article — the contrast between the two is more instructive than either alone.
https://www.investopedia.com/terms/s/sortinoratio.asp
*10 min*

**13. "Backtesting Systematic Trading Strategies in Python: Common Pitfalls and Remedies" — QuantStart**
If you test enough variations of a strategy on the same data, some will look good by chance. This is a mathematical certainty. The fix is out-of-sample testing. Read this before you write a single line of backtest code.
https://www.quantstart.com/articles/backtesting-systematic-trading-strategies-in-python-common-pitfalls-and-remedies/
*20 min*

**Video 4: "The Problem with Backtesting — Why Most Strategies Fail Live" (YouTube)**
Why historical performance and live performance routinely diverge, with real examples.
https://www.youtube.com/watch?v=94s0yYECeR8
*20 min*

---

**Before moving to Phase 3, do these two things:**

**Write your hypothesis.** Use this structure:

> *"When [observable condition X], I expect [asset Y] to [direction Z] over the next [N days], because [mechanism M]."*

The mechanism is the hard part. *"Stocks go up after this pattern"* is not a mechanism. *"When short-term momentum exceeds long-term momentum, recent buyers have unrealised gains and are likely to hold, reducing near-term selling pressure"* is. Write one you could actually implement.

**Answer this:** Someone tells you: *"I tested 200 variations of a moving average strategy on 5 years of data. The best one had a Sharpe of 2.1 and a max drawdown of 8%."* Write down three questions you'd ask before believing that result. At least one should be about what those metrics don't tell you.

---

## Phase 3: Tools and Task
*~2 hours to set up and start; rest of the week to complete the task*

No new concepts. Phase 3 is the bridge from ideas to code. Get the tooling in place, do the short warm-up, then build.

---

**Getting set up**

**14. "Time Series Analysis with Pandas" — Towards Data Science**
Date indexing, resampling, rolling windows — focused on financial time-series specifically. Slow down on rolling windows; you'll need them.
https://towardsdatascience.com/time-series-analysis-with-pandas-e6281a5fcda0
*20 min*

**15. "yfinance" — PyPI**
How you'll pull real market data. Read the README to understand what the library returns and how it's structured. Note the difference between `download()` for multiple tickers and `Ticker().history()` for a single name with more metadata.
https://pypi.org/project/yfinance/
*10 min*

---

**Before opening the notebook, answer these three questions in writing:**

1. Is your hypothesis specific enough to implement? If not, sharpen it now — vague hypotheses produce unreadable results.
2. What would falsify it? Name one concrete outcome from the data that would make you reject it. If you can't answer this, you don't have a hypothesis.
3. What does your benchmark look like? Before you see any results, write down what Sharpe ratio and max drawdown you'd expect from simply buying and holding your chosen asset.

---

## Week 1 Task

**Your First Signal Analysis — Jupyter Notebook**

Pull at least **3 years of daily price data** for any liquid stock or index of your choice using `yfinance`. Work through three parts.

---

**Part 1 — Return Profile and Benchmark (~25% of marks)**

- Compute daily log returns
- Plot the return distribution. Does it look normal? Where are the tails thicker than you'd expect?
- Report the following for the raw asset (buy-and-hold):
  - Mean daily return and annualised return
  - Annualised volatility (daily std × √252)
  - Annualised Sharpe ratio — use risk-free rate = 0, and note that this is a simplification
  - Maximum drawdown over the full sample period
  - Best and worst single day

This is your benchmark. Every number your signal produces in Part 2 gets compared to this.

---

**Part 2 — Your Signal (~50% of marks)**

State your hypothesis in a Markdown cell *before you show any results*. Then:

- Implement your signal — computable from price or volume data only, defined precisely enough that someone else could reimplement it from your description
- For each day, classify whether your signal is on or off (or above/below a threshold — define it clearly)
- Simulate a simple strategy: long when signal is on, flat when off
- Report for your signal strategy:
  - Average return over the next 5 trading days in each signal state — does the direction match your hypothesis?
  - Annualised return
  - Annualised Sharpe ratio
  - Maximum drawdown
- Compare all metrics side-by-side against the Part 1 benchmark

---

**Part 3 — Honest Assessment (~25% of marks)**

- What is the single biggest reason this result might not hold in live trading?
- How many genuinely independent observations does your sample contain for this signal? If your signal uses a 30-day rolling window, you don't have 3 × 252 = 756 independent data points. Work out approximately how many you do have, and explain why it matters for how much you should trust your Sharpe estimate.
- Looking at your Sharpe and drawdown numbers together: does your signal represent a genuine improvement over buy-and-hold, a tradeoff, or something worse on both dimensions? Be specific.

---

**Before submitting, check:**
- [ ] Hypothesis written before results, not after
- [ ] Log returns used throughout, not prices
- [ ] Ticker defined as a variable at the top, not hardcoded
- [ ] Sharpe computed correctly: annualised, risk-free rate stated
- [ ] Max drawdown computed from the equity curve, not the return series
- [ ] Each section has a Markdown cell explaining what you're doing and why
- [ ] Part 3 answered honestly — a bad result with good reasoning scores higher than a good result with no reasoning

**Format:** `.ipynb`, clean cell outputs, submitted by end of Week 1.

---

*The goal this week isn't a profitable strategy. It's a precise question, an honest answer, and the ability to read the numbers that tell you which is which.*

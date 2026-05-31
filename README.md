# CSOT Quant Finance & Research — Week 1

This week will cover:
1. An introduction to finance, markets, and where quant firms stand in all of this
2. The workflow of how a quantitative strategy is created, tested and deployed — then an insight into the components of a strategy
3. Introduction to some tools and a task for the week

This week has three phases. Work through them in order — each one feeds the next. Total time is **~8–10 hours**; you have the full week to finish.

---

## Phase 1: Understanding The Market

*Approximately 1–2 hours*

If you prefer reading: [Introduction to Stock Markets — Zerodha Varsity](https://zerodha.com/varsity/module/introduction-to-stock-markets/)

**Watch:**
- [How does the stock market work? — Oliver Elfenbaum](https://www.youtube.com/watch?v=p7HKvqRI_Bo)
- [Explained | The Stock Market | FULL EPISODE | Netflix](https://www.youtube.com/watch?v=ZCFkWDdmXG8)
- [Every Stock Market Terms Explained: Stock Market For Beginners](https://www.youtube.com/watch?v=EAKGuN-d07Q)

**Read:**
- [Stock Market Participants — Unity Wealth Capital](https://unitywealthcapital.com/stock-market-participants/)

**What do Quant Firms do:**
- [A $16B hedge fund CIO gives an easy explanation of quantitative trading](https://www.youtube.com/watch?v=85An6nPh2SI)
- [What is a Market Maker?](https://www.youtube.com/watch?v=x92YrwJ7MvQ)

### Types of Quant Firms

| Type | Description | Examples |
|------|-------------|---------|
| **Commercial Banks** | Offer financial products to retail/corporate clients; quant roles focus on risk modeling, derivatives pricing, and ALM. | JPMorgan, Goldman Sachs (banking division), HSBC, Citi |
| **Investment Banks** | Facilitate capital markets (IPOs, M&A, structured products); quants build pricing models and manage trading book risk. | Morgan Stanley, Barclays, Deutsche Bank, UBS |
| **Market Makers** | Continuously quote bid/ask prices to provide liquidity; profit from the spread and require ultra-fast, low-latency quant strategies. | — |
| **1. Hedge Funds** | Pool external capital, take directional or stat-arb positions with longer holding periods. | Citadel, Two Sigma, DE Shaw, Renaissance Technologies |
| **2. Prop Trading Firms** | Trade only the firm's own capital, often HFT-focused with extremely tight feedback loops. | Jane Street, Optiver, IMC, Virtu, Flow Traders |
| **Accountancy & Insurance Firms** | Use quants (actuaries) for risk assessment, liability pricing, and regulatory capital modeling. | Deloitte, PwC (quant consulting), Swiss Re, AXA, Zurich Insurance |
| **Exchanges** | Operate the trading infrastructure itself; quants work on market microstructure, surveillance, and matching engine optimization. | NSE, BSE, CME Group, Nasdaq, ICE |

**Other Resources:**
- [Hedge funds intro | Finance & Capital Markets | Khan Academy](https://www.youtube.com/watch?v=Qb7tbWuDc2U)
- [Buy Side vs Sell Side firms — r/quant](https://www.reddit.com/r/quant/comments/1g95ynl/a_discussion_on_sellside_vs_buyside/)

The market is huge!! In this track, we'll mainly focus on one thing: how to trade in a market if you are a trader. Particularly, how to use algorithms to trade on your behalf.

**In that spirit, let's get started!**

---

## Phase 2: Signals, Backtesting, and Measuring What Matters

*How it all comes together — ~3–4 hours | work through in order*

### What is a signal?

A signal is a condition derived from observable data — price, volume, open interest — that you believe predicts something about future returns. Not *"the stock will go up."* Something more precise: *when this condition is true, the next N days tend to look like this.*

**Watch:** [What is Quantitative Finance? 📈 Intro for Aspiring Quants](https://www.youtube.com/watch?v=JVtUcM1sWQw)

**Read through:**
- https://zerodha.com/varsity/module/trading-systems/
- https://www.quantstart.com/articles/Beginners-Guide-to-Quantitative-Trading/

### The anatomy of a strategy

Every quant strategy has three parts. They're separable — which matters, because a bad signal and a bad risk model can cancel each other out and look fine until they don't.

- **Alpha signal** — the thing you think predicts future returns. Could be price-based (momentum, mean reversion), fundamental (earnings yield), or micro-structural (order imbalance). Most signals are weak and noisy. That's fine. **Weak + uncorrelated is valuable. Weak + correlated with everything else is worthless.**

- **Position sizing / risk model** — how much to bet when the signal fires. Equal weight is fine to start. The point is that this is a separate decision from the signal itself — don't conflate them.

- **Execution** — when and how you actually enter and exit. Irrelevant for now since you're working with daily close prices. But keep in mind: a signal that needs you to trade 10 minutes after open behaves very differently from one that trades at close.

### Backtesting — what it is and why it lies to you

A backtest simulates your strategy on historical data to estimate how it would have performed. It's the first filter — not the last. The results are almost always optimistic, for reasons that are worth understanding now rather than after you've fallen in love with a Sharpe of 3.

- **Lookahead bias** — accidentally using future information to make past decisions. Classic example: computing a signal with today's close and then trading at today's open. Easy to introduce, hard to spot.
- **Survivorship bias** — testing only on stocks that exist today means your universe excludes every company that went bankrupt, got delisted, or merged. Your backtest thinks those winners were always winners.
- **Overfitting** — the more parameters you tune, the more your strategy fits historical noise rather than real structure. A strategy with 2 parameters tested on 3 years of data is in a different risk category than one with 12 parameters on the same data.
- **Transaction costs** — daily-rebalancing strategies that look good on paper often get eaten alive by bid-ask spreads and market impact once you account for actual execution costs.

> The correct mental model: a backtest tells you **whether your hypothesis is consistent with historical data**, not whether you'll make money. Those are different questions.

### The metrics that matter (and what they hide)

These four numbers show up everywhere. Know what each one is actually measuring — and what it isn't.

- **Sharpe Ratio** = (Mean excess return) / (Std dev of returns), annualised. Measures return per unit of volatility. A Sharpe above 1 is decent for a daily strategy; above 2 should make you suspicious. What it *doesn't* tell you: whether your returns are normally distributed (they're not), how the strategy behaves in tail events, or how much of it is luck.

- **Maximum Drawdown** = The peak-to-trough decline on the equity curve. If your strategy grows ₹100 → ₹150 → ₹90, the max drawdown is 40%. This is the number your risk tolerance needs to survive. Sharpe can look fine while max drawdown is completely unacceptable.

- **Annualised Return** — straightforward, but always compare it to a benchmark. A 12% annualised return sounds good until the index returned 18% over the same period.

- **Number of independent observations** — this one's under-discussed. If your signal uses a 20-day rolling window and you test on 3 years of daily data, you don't have 756 independent signal observations. You have roughly 756/20 ≈ 38. Your Sharpe estimate has enormous uncertainty around it. This matters because a Sharpe of 2.1 computed over 38 independent observations is consistent with a true Sharpe anywhere from 0.5 to 4+.

### Before you move to Phase 3

Two things to do before you open a notebook:

**1. Write your hypothesis.** Use this structure:

> *"When [observable condition X], I expect [asset Y] to [direction Z] over the next [N days], because [mechanism M]."*

The mechanism is the hard part. "Stocks go up after this pattern" is not a mechanism. "When short-term momentum exceeds long-term momentum, recent buyers have unrealised gains and are likely to hold, reducing near-term selling pressure" is. Write one you could actually implement.

**2. Answer this:** Someone tells you: *"I tested 200 variations of a moving average strategy on 5 years of data. The best one had a Sharpe of 2.1 and a max drawdown of 8%."* Write down three questions you'd ask before believing that result. At least one should be about what those metrics don't tell you.

---

## Phase 3: Tools and Task

*~2 hours to set up and start; rest of the week to complete the task*

No new concepts. Phase 3 is the bridge from ideas to code. Get the tooling in place, do the short warm-up, then build.

### Getting set up

| # | Resource | Notes | Time |
|---|----------|-------|------|
| 1 | [Time Series Analysis with Pandas — Towards Data Science](https://towardsdatascience.com/time-series-analysis-with-pandas-e6281a5fcda0) | Date indexing, resampling, rolling windows — focused on financial time-series specifically. Slow down on rolling windows; you'll need them. | 20 min |
| 2 | [yfinance — PyPI](https://pypi.org/project/yfinance/) | How you'll pull real market data. Read the README to understand what the library returns and how it's structured. Note the difference between `download()` for multiple tickers and `Ticker().history()` for a single name with more metadata. | 10 min |

Before opening the notebook, think through these three questions:

- **Is your hypothesis specific enough to implement?** If not, sharpen it now — vague hypotheses produce unreadable results.
- **What would falsify it?** Name one concrete outcome from the data that would make you reject it. If you can't answer this, you don't have a hypothesis.
- **What does your benchmark look like?** Before you see any results, write down what Sharpe ratio and max drawdown you'd expect from simply buying and holding your chosen asset.

---

## Week 1 Task

### Your First Signal Analysis — Jupyter Notebook

Pull at least 3 years of daily price data for any liquid stock or index of your choice using `yfinance`. Work through three parts.

---

### Part 1 — Return Profile and Benchmark
*~25% of marks*

Compute daily log returns.

Plot the return distribution. Does it look normal? Where are the tails thicker than you'd expect?

Report the following for the raw asset (buy-and-hold):
- Mean daily return and annualised return
- Annualised volatility (daily std × √252)
- Annualised Sharpe ratio — use risk-free rate = 0, and note that this is a simplification
- Maximum drawdown over the full sample period
- Best and worst single day

**This is your benchmark. Every number your signal produces in Part 2 gets compared to this.**

---

### Part 2 — Your Signal
*~50% of marks*

State your hypothesis in a Markdown cell before you show any results. Then:

- **Implement your signal** — computable from price or volume data only, defined precisely enough that someone else could reimplement it from your description
- For each day, classify whether your signal is **on** or **off** (or above/below a threshold — define it clearly)
- Simulate a simple strategy: long when signal is on, flat when off

Report for your signal strategy:
- Average return over the next 5 trading days in each signal state — does the direction match your hypothesis?
- Annualised return
- Annualised Sharpe ratio
- Maximum drawdown

Compare all metrics side-by-side against the Part 1 benchmark.

---

### Part 3 — Honest Assessment
*~25% of marks*

- What is the single biggest reason this result might not hold in live trading?
- How many genuinely independent observations does your sample contain for this signal? If your signal uses a 30-day rolling window, you don't have 3 × 252 = 756 independent data points. Work out approximately how many you do have, and explain why it matters for how much you should trust your Sharpe estimate.
- Looking at your Sharpe and drawdown numbers together: does your signal represent a genuine improvement over buy-and-hold, a tradeoff, or something worse on both dimensions? Be specific.

---

### Before submitting, check:

- [ ] Hypothesis written before results, not after
- [ ] Log returns used throughout, not prices
- [ ] Ticker defined as a variable at the top, not hardcoded
- [ ] Sharpe computed correctly: annualised, risk-free rate stated
- [ ] Max drawdown computed from the equity curve, not the return series
- [ ] Each section has a Markdown cell explaining what you're doing and why
- [ ] Part 3 answered honestly — a bad result with good reasoning scores higher than a good result with no reasoning

**Format:** `.ipynb`, clean cell outputs, submitted by end of Week 1.

---

> The goal this week isn't a profitable strategy. It's a precise question, an honest answer, and the ability to read the numbers that tell you which is which.

---

*Note: If you find any errors in this document, our apologies, and we would appreciate it if you let us know!*

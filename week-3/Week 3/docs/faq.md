# FAQ

**Can I use machine learning models, or does this have to be rule-based?**
Either is fine. Anything that only uses feature history strictly before the
current date is allowed — simple rules, factor scores, ML models, ensembles.

**Can I use external data (sector classifications, macro data, alternative
data, etc.)?**
No. Only the provided anonymized features may be used. The dataset is
anonymized specifically so stock identities aren't recoverable, so external
joins aren't possible anyway — but to keep the playing field level, external
data is not permitted.

**Why is the dollar-neutral constraint there?**
It forces the strategy to express a relative view (which stocks will do better
or worse than others) rather than a directional bet on the market as a whole.
A portfolio that's flat overall but long/short the right names can be
profitable even if the market doesn't move.

**What happens if my code doesn't reproduce my submitted `submission.csv`?**
Per `docs/competition_rules.md`, mismatched code/submission pairs are
disqualified — make sure you re-run end to end before your final submission.

**Can the set of tradable stocks change day to day?**
Yes — that's exactly what `universe.parquet` encodes. A stock can enter or
leave the tradable universe on any date; `get_weights` is told which stocks
are eligible *for that day* via `today_universe`.

**My strategy returns weights for a stock not in `today_universe` — what
happens?**
The backtest loop (`utils.backtest_strategy`) silently drops any such entries
and sets that stock's weight to 0 — but submissions that frequently do this
suggest a bug worth fixing before you submit.

**Where do I check my Sharpe ratio before submitting?**
Run `notebooks/main.ipynb` end to end — the last few cells compute Gross/Net
Sharpe and turnover using `data/returns.parquet`.

**When is the deadline?**
Final submissions are due **23 June, 11:59 PM**. The competition opens 16 June.
Only your last valid submission before the deadline is scored.

**How many submissions can I make, and what's the team size?**
You may submit as many times as you like before the deadline; only the last
valid one counts. Teams of up to 4 participants are allowed. (Organizers: adjust
this line if your rules differ.)

**Where do I get the data?**
See `data/download_data.md` — the parquet files are hosted on Google Drive and
are not committed to the repository.

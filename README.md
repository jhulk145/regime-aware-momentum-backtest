# Regime-Aware Momentum Backtest

A lightweight backtesting framework that compares a plain time-series momentum
strategy against a **volatility-regime-aware** version of the same strategy on
a single asset (default: SPY).

The core idea: momentum tends to work better in calm markets and can whipsaw
in high-volatility regimes. This project labels each day as `low_vol` or
`high_vol` based on rolling realized volatility, then down-weights the
momentum position on high-vol days instead of trading it at full size.

## How it works

1. **Data** — Daily adjusted close prices are pulled via `yfinance`.
2. **Signal** — A binary momentum signal: long (`1`) if the trailing N-day
   return is positive, flat (`0`) otherwise.
3. **Regime detection** — Rolling volatility (std of daily returns over a
   window) is compared to a quantile threshold to label each day `low_vol`
   or `high_vol`.
4. **Regime-aware weighting** — The momentum signal is scaled by a weight
   that depends on the current regime (e.g. full size in `low_vol`, reduced
   size in `high_vol`).
5. **Backtest** — Positions are lagged by one day and multiplied by realized
   returns, with a simple turnover-based transaction cost applied.
6. **Metrics** — Sharpe ratio, max drawdown, total return, and daily
   mean/vol are reported for both the baseline and regime-aware strategies.

## Project structure

```
.
├── run.py                  # Entry point — runs baseline vs. regime-aware backtest
├── requirements.txt
├── notebooks/
│   └── results.ipynb       # (scratch space for analysis/plots)
└── src/
    ├── data.py              # Price loading + return conversion
    ├── regimes.py           # Rolling volatility regime labeling
    ├── strategy.py          # Momentum signal + regime-based position sizing
    ├── backtest.py          # Long/flat backtest engine with transaction costs
    └── metrics.py           # Sharpe, max drawdown, summary stats
```

## Installation

```bash
git clone https://github.com/jhulk145/regime-aware-momentum-backtest.git
cd regime-aware-momentum-backtest
python -m venv .venv && source .venv/bin/activate  # optional but recommended
pip install -r requirements.txt
```

This project depends on:
- `pandas`
- `numpy`
- `yfinance`

> `requirements.txt` is currently empty — add the packages above (with
> versions pinned as you like) before installing.

## Usage

Run the default comparison (SPY, since 2015-01-01):

```bash
python run.py
```

This prints summary stats for both the baseline momentum strategy and the
regime-aware version, e.g.:

```
Baseline:      {'mean_daily': ..., 'vol_daily': ..., 'sharpe': ..., 'max_drawdown': ..., 'total_return': ..., 'n_days': ...}
Regime-aware:  {'mean_daily': ..., 'vol_daily': ..., 'sharpe': ..., 'max_drawdown': ..., 'total_return': ..., 'n_days': ...}
```

### Customizing a run

Edit the parameters at the top of `main()` in `run.py`:

| Parameter | Where | Default | Meaning |
|---|---|---|---|
| `ticker` | `run.py` | `"SPY"` | Symbol to backtest |
| `start` | `run.py` | `"2015-01-01"` | Backtest start date |
| `lookback` | `momentum_signal` | `126` | Momentum lookback window (trading days) |
| `window` | `rolling_vol_regime` | `20` | Rolling window for volatility estimate |
| `split` | `rolling_vol_regime` | `0.6` | Quantile threshold separating low/high vol |
| `low_weight` / `high_weight` | `apply_regime_weights` | `1.0` / `0.3` | Position size in each regime |
| `fee_bps` | `backtest_long_flat` | `1.0` | Transaction cost per unit of turnover, in basis points |

## Module reference

- **`src/data.py`**
  - `load_prices(ticker, start)` — downloads and returns a cleaned price series.
  - `to_returns(prices)` — converts prices to simple daily returns.
- **`src/regimes.py`**
  - `rolling_vol_regime(returns, window, split)` — labels each day `low_vol`
    or `high_vol` based on a rolling-volatility quantile split.
- **`src/strategy.py`**
  - `momentum_signal(prices, lookback)` — binary long/flat signal from
    trailing returns.
  - `apply_regime_filter(signal, regime, allow_regimes)` — zeroes out the
    signal outside the allowed regime(s) (hard on/off filter).
  - `apply_regime_weights(signal, regime, low_weight, high_weight)` — scales
    the signal by a regime-dependent weight (soft sizing; used in `run.py`).
- **`src/backtest.py`**
  - `backtest_long_flat(prices, signal, fee_bps)` — lags positions by one day,
    applies them to realized returns, and subtracts turnover-based costs.
- **`src/metrics.py`**
  - `sharpe(returns, periods_per_year)`, `max_drawdown(returns)`,
    `summary(returns)` — standard performance stats.

## Notes / caveats

- This is a research/educational backtest, not a production trading system —
  it ignores slippage beyond the flat `fee_bps` assumption, position limits,
  and market-impact effects.
- The regime split (`split=0.6`) is computed in-sample over the whole vol
  series, so there's look-ahead bias in the regime threshold itself; treat
  results as illustrative rather than a live-tradable edge.
- `apply_regime_filter` is implemented but not currently wired into `run.py`
  (which uses `apply_regime_weights` instead) — both are available if you
  want to compare a hard filter vs. soft sizing approach.

## License

No license specified yet — add one (e.g. MIT) if you intend for others to
reuse this code.
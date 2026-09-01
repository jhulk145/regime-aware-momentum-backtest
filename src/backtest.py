import pandas as pd

def _to_series(x, name=None) -> pd.Series:
    """Ensure x is a 1D Series."""
    if isinstance(x, pd.DataFrame):
        if x.shape[1] != 1:
            raise ValueError(f"Expected 1 column, got {x.shape[1]} columns: {list(x.columns)}")
        x = x.iloc[:, 0]
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    if name is not None:
        x.name = name
    return x

def backtest_long_flat(prices, signal: pd.Series, fee_bps: float = 0.0) -> pd.Series:
    """
    Simple daily backtest:
    - position = signal (0 or 1)
    - returns = position.shift(1) * daily_returns - trading_costs
    """
    prices = _to_series(prices, name="price")
    daily_ret = prices.pct_change().dropna()

    sig = _to_series(signal, name="pos").reindex(daily_ret.index).dropna()

    # Align
    df = pd.concat([daily_ret.rename("ret"), sig.rename("pos")], axis=1).dropna()

    # Trading cost on changes in position (enter/exit)
    turnover = df["pos"].diff().abs().fillna(0.0)
    cost = turnover * (fee_bps / 10000.0)

    strat_ret = df["pos"].shift(1).fillna(0.0) * df["ret"] - cost
    strat_ret.name = "strategy_return"
    return strat_ret

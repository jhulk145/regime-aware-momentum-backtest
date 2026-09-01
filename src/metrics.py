import numpy as np
import pandas as pd

def sharpe(returns: pd.Series, periods_per_year: int = 252) -> float:
    r = returns.dropna()
    if r.std() == 0:
        return 0.0
    return (r.mean() / r.std()) * np.sqrt(periods_per_year)

def max_drawdown(returns: pd.Series) -> float:
    r = returns.dropna()
    equity = (1 + r).cumprod()
    peak = equity.cummax()
    dd = (equity / peak) - 1.0
    return float(dd.min())

def summary(returns: pd.Series) -> dict:
    r = returns.dropna()
    out = {
        "mean_daily": float(r.mean()),
        "vol_daily": float(r.std()),
        "sharpe": float(sharpe(r)),
        "max_drawdown": float(max_drawdown(r)),
        "total_return": float((1 + r).prod() - 1),
        "n_days": int(r.shape[0]),
    }
    return out

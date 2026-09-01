import pandas as pd

def rolling_vol_regime(returns: pd.Series, window: int = 20, split: float = 0.5) -> pd.Series:
    """
    Volatility regime based on rolling volatility threshold.
    - Computes rolling std of returns
    - Uses quantile threshold (e.g. median=0.5) to define high vs low vol
    Returns a Series of regime labels: "low_vol" / "high_vol"
    """
    vol = returns.rolling(window).std().dropna()
    thresh = vol.quantile(split)
    regime = pd.Series(index=vol.index, dtype="object")
    regime[vol <= thresh] = "low_vol"
    regime[vol > thresh] = "high_vol"
    regime.name = "regime"
    return regime

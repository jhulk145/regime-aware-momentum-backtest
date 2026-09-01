import pandas as pd

def momentum_signal(prices: pd.Series, lookback: int = 126) -> pd.Series:
    past_ret = prices.pct_change(lookback)
    sig = (past_ret > 0).astype(int)  # 1 if positive momentum else 0
    sig = sig.dropna()
    sig.name = "signal"
    return sig

def apply_regime_filter(signal: pd.Series, regime: pd.Series, allow_regimes=("low_vol",)) -> pd.Series:
    """
    Only allow positions during specific regimes (default: low_vol).
    Returns a 0/1 Series aligned to dates where both signal and regime exist.
    """
    sig_df = signal.rename("signal").to_frame()
    reg_df = regime.rename("regime").to_frame()
    aligned = sig_df.join(reg_df, how="inner")

    filt = aligned["signal"].where(aligned["regime"].isin(allow_regimes), 0)
    filt.name = "signal_filtered"
    return filt

def apply_regime_weights(signal, regime, low_weight=1.0, high_weight=0.3):
    sig_df = signal.rename("signal").to_frame()
    reg_df = regime.rename("regime").to_frame()
    aligned = sig_df.join(reg_df, how="inner")

    w = aligned["regime"].map(
        {"low_vol": low_weight, "high_vol": high_weight}
    ).fillna(high_weight)

    weighted = aligned["signal"] * w
    weighted.name = "position"
    return weighted

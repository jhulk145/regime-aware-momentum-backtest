from src.data import load_prices
from src.regimes import rolling_vol_regime
from src.strategy import momentum_signal, apply_regime_weights
from src.backtest import backtest_long_flat
from src.metrics import summary

def main():
    ticker = "SPY"
    prices = load_prices(ticker, start="2015-01-01").squeeze()

    # Baseline momentum
    sig_base = momentum_signal(prices, lookback=126)
    ret_base = backtest_long_flat(prices, sig_base, fee_bps=1.0)

    # Volatility regime
    daily_ret = prices.pct_change().dropna()
    regime = rolling_vol_regime(daily_ret, window=20, split=0.6)

    # Regime-aware momentum (only trade in low vol)
    sig_reg = apply_regime_weights(
    sig_base,
    regime,
    low_weight=1.0,
    high_weight=0.3
)
    ret_reg = backtest_long_flat(prices, sig_reg, fee_bps=1.0)

    print("Baseline:", summary(ret_base))
    print("Regime-aware:", summary(ret_reg))
    print(type(prices), getattr(prices, "shape", None))

if __name__ == "__main__":
    main()

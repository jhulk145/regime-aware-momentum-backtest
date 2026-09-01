import pandas as pd
import yfinance as yf

def load_prices(ticker: str, start: str = "2015-01-01") -> pd.Series:
    df = yf.download(ticker, start=start, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for ticker: {ticker}")
    # Use Adjusted Close when available
    price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
    prices = df[price_col].dropna()
    prices.name = ticker
    return prices

def to_returns(prices: pd.Series) -> pd.Series:
    rets = prices.pct_change().dropna()
    rets.name = f"{prices.name}_ret"
    return rets

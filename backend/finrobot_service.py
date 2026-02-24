import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path

def analyze_company(symbol: str):
    """
    Fetches real-time market data from Yahoo Finance and applies 
    FinRobot investment logic.
    """
    # Clean the input (remove spaces and make uppercase)
    ticker_symbol = symbol.strip().upper()
    
    # 1. FETCH LIVE DATA FROM THE WEB
    # We download 1 year of daily historical data
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period="1y")

    # If yfinance returns an empty dataframe, the ticker is invalid or delisted
    if df.empty:
        raise ValueError(f"Ticker '{ticker_symbol}' not found online. Try AAPL, MSFT, or TCS.NS")

    # 2. DATA PREPARATION
    # Create the 'ret' column (Daily Percentage Change)
    df['close'] = df['Close']
    df['ret'] = df['close'].pct_change()
    
    # Drop the first row (NaN) so calculations don't break
    df = df.dropna()

    # 3. CALCULATE METRICS
    # Average daily return
    avg_return = df["ret"].mean()
    
    # Daily volatility (Standard Deviation of returns)
    volatility = df["ret"].std()
    
    # Total return over the last year: (Last Price / First Price) - 1
    total_return = (df["close"].iloc[-1] / df["close"].iloc[0]) - 1

    # 4. INVESTMENT LOGIC (Your custom criteria)
    if total_return > 0.2 and volatility < 0.03:
        decision = "INVEST"
    elif total_return > 0:
        decision = "HOLD"
    else:
        decision = "AVOID"

    # 5. DATA OUTPUT
    # Returns a dictionary formatted for the FastAPI backend
    return {
        "symbol": ticker_symbol,
        "avg_return": float(round(avg_return, 6)),
        "volatility": float(round(volatility, 6)),
        "total_return": float(round(total_return, 4)),
        "current_price": float(round(df["close"].iloc[-1], 2)),
        "decision": decision,
        "environment": "FinRobot Online Engine"
    }
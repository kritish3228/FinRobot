import pandas as pd
from pathlib import Path
import finrobot  

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "unified_market_data.csv"

REQUIRED_COLUMNS = {
    "date", "symbol", "close", "currency",
    "ret", "log_ret", "volume"
}

def load_market_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df


def analyze_company(symbol: str):
    df = load_market_data()
    data = df[df["symbol"] == symbol]

    if data.empty:
        raise ValueError("Company not found in provided historical data")

    avg_return = data["ret"].mean()
    volatility = data["ret"].std()
    total_return = (1 + data["ret"]).prod() - 1

    if total_return > 0.2 and volatility < 0.03:
        decision = "INVEST"
    elif total_return > 0:
        decision = "HOLD"
    else:
        decision = "AVOID"

    return {
        "symbol": symbol,
        "avg_return": round(avg_return, 6),
        "volatility": round(volatility, 6),
        "total_return": round(total_return, 4),
        "decision": decision,
        "environment": "FinRobot"
    }

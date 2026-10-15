import pandas as pd
from pathlib import Path


def historical_forecast(
    df: pd.DataFrame,
    window: int = 20,
    horizon: int = 5
) -> pd.Series:
    return horizon * df["log_return"].pow(2).rolling(window).mean()


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    source = root / "data/processed/market_returns.csv"

    df = pd.read_csv(source)

    print(df.head(5))

    print(df["log_return"][0:8])

import pandas as pd
from math import log1p, isfinite


def load_market_returns(path):
    df = pd.read_csv(path, skiprows=4, skipfooter=1, engine='python')
    df = df.rename(columns={"Unnamed: 0": "Date"})
    df["Date"] = pd.to_datetime(df["Date"].astype(str), format="%Y%m%d")
    df = df.loc[df["Date"] >= "2000-01-01", ["Date", "Mkt-RF", "RF"]].copy()
    df = df.reset_index(drop=True)
    df["simple_return"] = (df["Mkt-RF"] + df["RF"]) / 100

    if df.isna().any().any():
        raise ValueError("Missing values")

    if df["Date"].duplicated().any():
        raise ValueError("Duplicate dates")

    if not df["Date"].is_monotonic_increasing:
        raise ValueError("Dates not monotonic")

    if not (df["simple_return"] > -1).all():
        raise ValueError("Invalid simple returns")

    df["log_return"] = df["simple_return"].map(log1p)

    if not df["log_return"].map(isfinite).all():
        raise ValueError("Non-finite log returns")
    return df


if __name__ == "__main__":
    df = load_market_returns(
        "volatility-forecasting/data/raw/F-F_Research_Data_Factors_daily.csv")

    print(df.head())
    print(df.tail())
    print(df.shape)
    print(df.columns)
    print(df.dtypes)
    print(df[["simple_return", "log_return"]].describe())

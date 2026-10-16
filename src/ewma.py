import pandas as pd
from pathlib import Path


def ewma_forecast(
    df: pd.DataFrame,
    decay: float = 0.94,
    window: int = 20,
    horizon: int = 5
) -> pd.Series:
    initial_variance = df["log_return"].iloc[:20].pow(2).mean()
    variance = pd.Series(float("nan"), index=df.index)
    variance.iloc[19] = initial_variance

    for i in range(20, len(df)):
        variance.iloc[i] = (
            decay * variance.iloc[i-1] +
            (1 - decay) * df["log_return"].iloc[i]**2)

    return horizon * variance

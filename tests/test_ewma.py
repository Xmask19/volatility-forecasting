import pandas as pd
import pytest
from src.ewma import ewma_forecast


def test_ewma_initialisation():
    df = pd.DataFrame({
        "log_return": [0.01] * 19 + [0.02, -0.03]
    })

    forecast = ewma_forecast(df, window=20, horizon=5)

    # First 19 observations have insufficient history
    assert forecast.iloc[:19].isna().all()

    # Initial variance is the mean of 20 squared returns
    expected_variance = (19 * 0.01**2 + 0.02**2) / 20

    # Function returns cumulative five-day variance
    assert forecast.iloc[19] == pytest.approx(5 * expected_variance)

    assert forecast.iloc[20] == pytest.approx(
        0.94 * forecast.iloc[19] + 0.06 * 5 * df["log_return"].iloc[20]**2)


def test_ewma_no_lookahead():
    df = pd.DataFrame({
        "log_return": [0.01] * 20 + [0.02, 0.03]
    })

    original = ewma_forecast(df)

    # Change a future return
    df.loc[21, "log_return"] = 0.50
    modified = ewma_forecast(df)

    # Forecast at index 20 must remain unchanged
    assert modified.iloc[20] == pytest.approx(original.iloc[20])

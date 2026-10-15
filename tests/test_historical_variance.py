
import pandas as pd
import pytest

from src.historical_variance import historical_forecast


def test_historical_forecast():
    df = pd.DataFrame({
        "log_return": [0.01, -0.02, 0.03, 0.04]
    })

    forecast = historical_forecast(df, window=3, horizon=5)

    # Insufficient history for the first two days
    assert pd.isna(forecast.iloc[0])
    assert pd.isna(forecast.iloc[1])

    # Third day: mean of three squared returns, times five
    expected = 5 * (0.01**2 + (-0.02)**2 + 0.03**2) / 3
    assert forecast.iloc[2] == pytest.approx(expected)


def test_no_lookahead():
    df = pd.DataFrame({
        "log_return": [0.01, -0.02, 0.03, 0.04]
    })

    original = historical_forecast(df, window=3)

    # Change a return from the future
    df.loc[3, "log_return"] = 0.50

    modified = historical_forecast(df, window=3)

    # The forecast at day 3 must remain unchanged
    assert modified.iloc[2] == pytest.approx(original.iloc[2])

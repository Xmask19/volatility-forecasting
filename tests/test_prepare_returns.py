from pathlib import Path
import pytest
from src.prepare_returns import load_market_returns
from math import log1p

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("path", sorted(FIXTURES.glob("*.csv")))
def test_fixtures(path):
    if path.name.startswith("invalid_"):
        with pytest.raises(ValueError):
            load_market_returns(path)
    else:
        df = load_market_returns(path)
        assert not df.empty


def test_return_values():
    path = FIXTURES / "valid_01_date_filter_and_returns.csv"
    df = load_market_returns(path)

    # Two observations from 1999 should be excluded
    assert len(df) == 3
    assert df.loc[0, "Date"].strftime("%Y-%m-%d") == "2000-01-03"

    # 3 January 2000: Mkt-RF = -0.71, RF = 0.02
    assert df.loc[0, "simple_return"] == pytest.approx(-0.0069)
    assert df.loc[0, "log_return"] == pytest.approx(log1p(-0.0069))

    # 4 January 2000: Mkt-RF = -4.06, RF = 0.02
    assert df.loc[1, "simple_return"] == pytest.approx(-0.0404)
    assert df.loc[1, "log_return"] == pytest.approx(log1p(-0.0404))

    # 5 January 2000: Mkt-RF = 0.50, RF = 0.01
    assert df.loc[2, "simple_return"] == pytest.approx(0.0051)

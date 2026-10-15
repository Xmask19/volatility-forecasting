# Return-preprocessing test fixtures

These eight **synthetic** CSV files test the data-loading and validation logic in `src/prepare_returns.py`. They contain no observations copied from the Kenneth R. French Data Library.

## File format

Each file follows the relevant structure of the Fama/French 3 Factors daily CSV:

- Four introductory lines before the data header.
- `Date`, `Mkt-RF` and `RF` columns, with dates in `YYYYMMDD` format and returns in percentage points.
- One final line containing exactly `Synthetic test fixture`, to exercise the loader's footer handling.

## Test cases

| Fixture | Expected behaviour |
| --- | --- |
| `valid_01_date_filter_and_returns.csv` | Loads successfully; retains three in-range observations and converts market returns correctly. |
| `valid_02_zero_positive_negative.csv` | Loads successfully; handles zero, positive and negative returns. |
| `invalid_01_duplicate_dates.csv` | Rejects duplicate dates. |
| `invalid_02_unsorted_dates.csv` | Rejects dates that are not in ascending order. |
| `invalid_03_missing_market_return.csv` | Rejects a missing market-return value. |
| `invalid_04_below_minus_100_percent.csv` | Rejects a market return below −100%, for which a real-valued log return is undefined. |
| `invalid_05_infinite_return.csv` | Rejects a non-finite return. |
| `invalid_06_impossible_date.csv` | Rejects an invalid calendar date. |

For `valid_01_date_filter_and_returns.csv`, the three retained simple market returns, in date order, are `-0.0069`, `-0.0404` and `0.0051`. Their expected log returns are `log1p` of those respective values. Market returns are constructed from `(Mkt-RF + RF) / 100` before conversion to log returns.

Run the tests from the repository root with:

```bash
python -m pytest -q
```
# Data

## Source

The study uses [Fama/French 3 Factors [Daily]](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) from the Kenneth R. French Data Library.

- **Data vintage:** August 2026 CRSP, with observations through 31 August 2026.
- **Research sample:** January 2000–August 2026.
- **Required columns:** `Date`, `Mkt-RF`, `RF`.

Later downloads may contain revised historical observations.

## Data preparation

Download [`F-F_Research_Data_Factors_daily_CSV.zip`](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip).

Extract `F-F_Research_Data_Factors_daily.csv` into `data/raw/`.

Run from the repository root:

```bash
python -m src.prepare_returns
```

Output: `data/processed/market_returns.csv`.

Both data directories are excluded from Git.

## Return construction

Daily simple market returns are calculated from the percentage-point values:

`simple_return = (Mkt-RF + RF) / 100`

Daily log returns are then calculated as:

`log_return = log(1 + simple_return)`
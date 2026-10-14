# Data

## Source

Kenneth R. French Data Library — Fama/French 3 Factors [Daily].

https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

Official download:
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip

## Initial dataset

- Source database: August 2026 CRSP
- Available observations: 1 July 1926 – 31 August 2026
- Intended research sample: January 2000 onwards
- Required columns: Date, Mkt-RF, RF
- Original filename: `F-F_Research_Data_Factors_daily.csv`

Daily US market simple returns are calculated by adding Mkt-RF and RF, converting the published percentage values to decimals.

Daily log returns are calculated as:

`log(1 + market_return)`

## Local file locations

- `data/raw/` — original downloaded data
- `data/processed/` — derived research data

These directories are excluded from Git.

The source and processed datasets are not redistributed. Scripts for downloading and processing the data will be added as implementation progresses.

Historical source data may be revised. The download date and source-file checksum should be recorded when the automated data pipeline is implemented.
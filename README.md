# Volatility Forecasting

An empirical study of short-horizon US equity-market variance forecasting, comparing exponentially weighted moving average (EWMA) and GARCH(1,1) models with rolling historical variance as a reference.

## Research question

**To what extent does fitted GARCH(1,1) improve short-horizon variance forecasts over calibrated EWMA, and how do any differences relate to volatility persistence and mean reversion?**

EWMA is an integrated boundary case of GARCH(1,1). Stationary GARCH allows conditional variance to revert towards a long-run level, but this additional flexibility also requires more parameter estimation. The project examines whether it improves out-of-sample forecasts in practice.

## Study design

The core study compares:

- **Rolling historical variance:** a simple benchmark using recent squared returns.
- **EWMA:** a conventional decay factor of 0.94 and a factor calibrated on validation data.
- **GARCH(1,1):** a stationary model fitted by Gaussian maximum likelihood.

The **primary comparison** is between fitted GARCH and EWMA calibrated using **five-day validation QLIKE**. Forecasts are evaluated over non-overlapping five-trading-day periods, with QLIKE as the primary loss measure and RMSE as a secondary measure. One-day forecasts provide an additional comparison.

The chronological sample is divided into training (2000–2018), validation (2019–2021) and held-out testing (2022–August 2026). Estimated GARCH persistence and forecast paths are examined when interpreting model differences.

Controlled simulations and additional volatility models are possible extensions, not requirements of the core study.

## Data

The study uses **Fama/French 3 Factors [Daily]** from the [Kenneth R. French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). Market returns are constructed from the `Mkt-RF` and `RF` columns and converted to daily log returns.

The initial source file uses the **August 2026 CRSP database vintage**. The intended research sample begins in January 2000 and runs through August 2026.

The raw dataset and derived daily-return series are **not distributed in this repository**. See [data/README.md](data/README.md) for the official download link, source details and local file locations.

## Documentation

The [research specification (v0.4)](docs/research-specification.md) describes the mathematical framework, estimation procedures, evaluation design, limitations and optional extensions.

## Project status

**Initial research setup.** The research design has been documented and the source dataset obtained. Data-processing code, forecasting implementations, tests and empirical results have not yet been added. Reproduction instructions and findings will be included as the work progresses.

This is a research project on **variance forecasting**, not return-direction prediction or a trading strategy.
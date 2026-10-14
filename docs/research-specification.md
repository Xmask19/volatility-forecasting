# Volatility Forecasting — Research Specification

**Version:** 0.4  
**Date:** 14 October 2026  
**Status:** Proposed research design

## 1. Introduction

Financial returns exhibit volatility clustering: periods of large price movements tend to be followed by further periods of elevated volatility. Forecasting this time-varying uncertainty is an important problem in financial econometrics, with applications in risk management, derivative pricing and portfolio construction.

Exponentially Weighted Moving Average (EWMA) and Generalised Autoregressive Conditional Heteroskedasticity (GARCH) are two approaches to modelling conditional variance.

The models are closely related. EWMA corresponds to an integrated boundary case of GARCH(1,1), whereas a stationary GARCH model additionally allows expected conditional variance to revert towards a long-run level.

This additional flexibility may improve forecasting accuracy. However, GARCH requires the estimation of more parameters, introducing uncertainty that can offset the benefits of a more flexible specification.

The central research question is:

**To what extent does fitted GARCH(1,1) improve short-horizon variance forecasts over calibrated EWMA, and how do any differences relate to volatility persistence and mean reversion?**

The primary investigation compares five-trading-day variance forecasts using historical US equity-market returns. One-day forecasting provides a secondary comparison, while rolling historical variance serves as a simpler reference model.

An optional simulation study extends the investigation to processes with known conditional variance.

The objective is to evaluate forecasting performance and understand the sources of any differences, rather than establish the superiority of a particular model.

## 2. Mathematical framework

### 2.1 GARCH and EWMA

Assuming zero conditional mean returns, GARCH(1,1) is defined by

$$
r_t=\sigma_tz_t,
\qquad z_t\sim N(0,1),
$$

$$
\sigma_{t+1}^2
=
\omega+\alpha r_t^2+\beta\sigma_t^2,
$$

where the innovations are independent and standardised.

For the stationary specification considered here,

$$
\omega>0,\qquad
\alpha,\beta\ge0,\qquad
\alpha+\beta<1.
$$

The long-run unconditional variance is

$$
\bar{\sigma}^2
=
\frac{\omega}{1-\alpha-\beta}.
$$

EWMA instead follows

$$
\sigma_{t+1}^2
=
(1-\lambda)r_t^2+\lambda\sigma_t^2,
\qquad 0<\lambda<1.
$$

This is equivalent to the parameter restrictions

$$
\omega=0,\qquad
\alpha=1-\lambda,\qquad
\beta=\lambda,
$$

which imply

$$
\alpha+\beta=1.
$$

EWMA therefore lies on the integrated boundary rather than within the stationary GARCH parameter space. Nevertheless, a fitted stationary GARCH model may approach this boundary closely.

### 2.2 Persistence and multi-period forecasting

Let

$$
\rho=\alpha+\beta
$$

denote GARCH persistence, and let \(v_t\) represent its one-step-ahead variance forecast at time \(t\).

The expected conditional variance \(j\) trading days ahead is

$$
E_t[\sigma_{t+j}^2]
=
\bar{\sigma}^2+
\rho^{j-1}(v_t-\bar{\sigma}^2).
$$

Consequently, the cumulative variance forecast over \(h\) trading days is

$$
\widehat V_{t,h}^{\mathrm{GARCH}}
=
h\bar{\sigma}^2+
(v_t-\bar{\sigma}^2)
\frac{1-\rho^h}{1-\rho}.
$$

Under EWMA, the corresponding forecast is

$$
\widehat V_{t,h}^{\mathrm{EWMA}}
=
h v_t^{\mathrm{EWMA}}.
$$

GARCH allows expected variance to revert towards a long-run level, whereas EWMA maintains the current expected daily variance over the forecast horizon.

For equal one-step-ahead forecasts, the difference between their multi-period predictions tends to disappear as GARCH persistence approaches one.

In practice, fitted forecasts may also differ because of their current variance estimates and estimation procedures. A difference in forecasting accuracy does not, by itself, isolate the contribution of mean reversion.

## 3. Data

### 3.1 Source and sample

The empirical analysis uses daily US equity-market returns from the [Kenneth R. French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html), specifically the **Fama/French 3 Factors [Daily]** dataset.

The initial downloaded file uses the August 2026 CRSP database vintage, with observations through 31 August 2026.

The research sample covers January 2000 to August 2026, comprising 6,705 daily observations.

The market series represents a broad value-weighted US equity portfolio rather than the S&P 500 index or a directly investable fund.

Historical observations may be revised by the data provider. The source and database vintage identify the dataset used in the investigation.

### 3.2 Return construction

The relevant dataset fields are:

- `Date`: Trading date.
- `Mkt-RF`: Market excess return.
- `RF`: Risk-free return.

The published returns are expressed in percentage points.

Daily simple market returns are constructed as

$$
R_t
=
\frac{(Mkt-RF)_t+RF_t}{100},
$$

with log returns defined by

$$
r_t=\log(1+R_t).
$$

The analysis uses decimal log returns throughout.

The data-processing procedure includes checks for duplicate dates, invalid numerical observations, chronological ordering and correct return transformations.

The original dataset remains unchanged. Raw and processed daily-return series are stored locally, while the public repository contains the code and instructions required to reproduce their construction.

## 4. Forecasting models

Three models form the core empirical comparison.

### 4.1 Rolling historical variance

Rolling historical variance estimates the current daily variance from recent squared returns:

$$
\widehat{\sigma}_t^2
=
\frac1n
\sum_{i=0}^{n-1}r_{t-i}^2.
$$

The primary reference uses a 20-trading-day window, approximately one trading month.

Assuming constant expected daily variance over the forecast horizon,

$$
\widehat V_{t,h}
=
h\widehat{\sigma}_t^2.
$$

A 60-day window provides a secondary sensitivity comparison.

### 4.2 EWMA

EWMA estimates conditional variance recursively:

$$
\widehat{\sigma}_{t+1}^2
=
\lambda\widehat{\sigma}_t^2
+
(1-\lambda)r_t^2.
$$

Two specifications are considered.

**Conventional EWMA** uses the daily RiskMetrics decay parameter

$$
\lambda=0.94.
$$

**Calibrated EWMA** uses a decay parameter selected from validation-period forecasting performance.

The five-day cumulative forecast is

$$
\widehat V_{t,5}
=
5\widehat{\sigma}_{t+1}^2.
$$

The conventional model provides a fixed reference, while the calibrated model forms the principal comparison against GARCH.

### 4.3 GARCH(1,1)

The GARCH model follows the conditional-variance recursion introduced in Section 2.

Its parameters are estimated using Gaussian maximum likelihood, subject to the stated positivity and stationarity restrictions.

Estimation uses an expanding historical window, with parameter re-estimation every 20 trading days. Between re-estimations, newly observed returns update the conditional variance state.

Multi-period forecasts are calculated using the fitted recursion.

The estimated persistence,

$$
\widehat{\rho}
=
\widehat{\alpha}+\widehat{\beta},
$$

and implied long-run variance are of particular interest because they characterise the model's estimated mean-reverting behaviour.

## 5. Calibration and experimental design

### 5.1 EWMA calibration

The EWMA decay parameter is selected by minimising five-day QLIKE loss over the validation sample.

For a forecast originating at the close of day \(t\), realised variance over the next five trading days is

$$
RV_{t,5}
=
\sum_{j=1}^{5}r_{t+j}^2.
$$

The calibrated parameter is

$$
\lambda^*
=
\arg\min_{\lambda\in\Lambda}
\frac1N
\sum_{t\in\mathcal T_{\mathrm{val}}}
\left[
\log\widehat V_{t,5}(\lambda)
+
\frac{RV_{t,5}}{\widehat V_{t,5}(\lambda)}
\right],
$$

where

$$
\Lambda=\{0.900,0.905,\ldots,0.990\}.
$$

Calibration uses non-overlapping five-trading-day validation targets, matching the primary evaluation horizon and loss function.

EWMA variance estimates continue to update daily, using information available at each forecast origin.

The selected value of \(\lambda^*\) remains fixed during the final test period.

### 5.2 Sample division

The historical sample is divided chronologically.

| Period | Dates | Purpose |
|---|---|---|
| Training | 2000–2018 | Initial model development and estimation |
| Validation | 2019–2021 | EWMA calibration and methodological decisions |
| Test | 2022–August 2026 | Final out-of-sample evaluation |

The final period is a retrospective holdout rather than a genuinely prospective experiment.

During validation and testing, GARCH parameters and variance states may incorporate newly observed returns. This reflects the information that would have been available at each historical forecast origin.

Test-period forecast losses are excluded from model selection and calibration decisions.

### 5.3 Forecast scheduling

Five-day forecasts are evaluated over non-overlapping blocks of five trading days.

The first forecast originates at the final trading-day close before the relevant evaluation period, followed by a new forecast every five trading days.

One-day forecasts are evaluated at each eligible trading-day close.

All models use identical forecast origins and realised-variance targets for a given horizon. Only complete forecast horizons enter the evaluation.

Although five-day targets do not overlap, successive forecast-loss observations may remain serially dependent.

### 5.4 Estimation considerations

The primary comparison involves EWMA calibrated using validation-period QLIKE and GARCH estimated using Gaussian maximum likelihood.

These procedures use different parameter-estimation criteria. The comparison therefore concerns the forecasting performance of two specified modelling procedures, rather than the isolated causal effect of mean reversion.

Differences between fitted one-step variance estimates and multi-step forecast dynamics are considered when interpreting the results.

## 6. Forecast evaluation

### 6.1 Forecast target

The intended forecasting quantity is cumulative conditional variance over the horizon:

$$
V^*_{t,h}
=
E_t\left[
\sum_{j=1}^{h}\sigma_{t+j}^2
\right].
$$

Under the zero conditional mean assumption and appropriate moment conditions,

$$
E_t[RV_{t,h}]=V^*_{t,h},
$$

where

$$
RV_{t,h}
=
\sum_{j=1}^{h}r_{t+j}^2.
$$

Realised variance therefore provides an observable but noisy proxy for the underlying forecasting target.

### 6.2 Primary loss: QLIKE

Forecast accuracy is assessed primarily using

$$
L_{\mathrm{QLIKE}}(\widehat V,RV)
=
\log(\widehat V)+\frac{RV}{\widehat V}.
$$

Forecast variances are strictly positive.

QLIKE has desirable properties for conditional-variance forecast comparison when realised variance is a suitably unbiased but imperfect proxy.

Lower average QLIKE indicates better performance under the chosen loss function.

The **primary empirical comparison** is between fitted GARCH(1,1) and validation-calibrated EWMA, evaluated on five-day test-period forecasts.

Conventional EWMA and historical variance provide additional benchmarks.

### 6.3 Secondary loss: RMSE

Root mean squared error provides a complementary evaluation:

$$
\operatorname{RMSE}
=
\sqrt{
\frac1N
\sum_t(\widehat V_t-RV_t)^2
}.
$$

Unlike QLIKE, RMSE places greater emphasis on large absolute variance forecast errors.

Differences between rankings under the two loss functions may provide information about the types of forecasting errors made by each model.

One-day results are reported separately from the primary five-day comparison.

### 6.4 Statistical inference

For each five-day forecast period, the paired QLIKE loss difference is

$$
d_t
=
L_{\mathrm{GARCH},t}
-
L_{\mathrm{EWMA},t}.
$$

The primary hypotheses are

$$
H_0:E[d_t]=0,
$$

$$
H_1:E[d_t]\ne0.
$$

A negative mean difference favours GARCH, while a positive difference favours EWMA.

The estimated mean loss difference is accompanied by a 95% confidence interval and a two-sided significance test.

A moving-block bootstrap is proposed to account for possible serial dependence in forecast-loss differences.

The bootstrap configuration is determined before final test evaluation.

Both statistical uncertainty and the magnitude of observed differences inform the conclusions. A failure to reject the null hypothesis is not equivalent to demonstrating equal forecasting accuracy.

## 7. Interpretation of empirical results

Three aspects of the results are of particular interest.

### 7.1 Relative forecasting accuracy

The primary analysis establishes whether fitted GARCH achieves lower five-day QLIKE loss than calibrated EWMA, and whether the observed difference is distinguishable from sampling uncertainty.

Performance relative to conventional EWMA and rolling historical variance provides additional context.

### 7.2 Estimated persistence

GARCH persistence determines the expected rate at which conditional variance reverts towards its long-run level.

Estimates close to one imply slow mean reversion and may produce multi-period forecasts resembling EWMA.

The analysis relates estimated persistence to observed forecast differences, while recognising that current variance estimates may differ between the models.

### 7.3 Forecast horizon

One-day and five-day comparisons provide evidence about whether additional modelling flexibility becomes more useful as the forecast horizon increases.

Mean reversion may influence longer-horizon forecasts more strongly, although statistical accuracy also depends on estimation uncertainty and the characteristics of observed returns.

These analyses are descriptive rather than attempts to establish a causal effect from historical forecast comparisons alone.

## 8. Limitations

Several considerations constrain the interpretation of the empirical findings.

**Unobservable conditional variance.** Realised variance derived from daily squared returns is a noisy proxy for the underlying conditional variance.

**Model assumptions.** Zero conditional mean returns, Gaussian innovations and the specified variance recursions simplify actual market behaviour.

**Near-integrated dynamics.** When estimated GARCH persistence approaches one, the strength of mean reversion and the implied long-run variance may be difficult to determine reliably.

**Estimation differences.** GARCH and EWMA are calibrated using different primary criteria, so forecasting differences cannot be attributed exclusively to model structure.

**Historical revisions.** The market-return series is retrospectively constructed and may be revised by the data provider.

**Changing market conditions.** Historical volatility dynamics may not remain stable across different economic environments.

**Evaluation sample size.** Non-overlapping five-day forecasts provide substantially fewer evaluation observations than daily forecasting, limiting precision.

**Generalisability.** Results for a broad US equity-market series may not transfer to other assets or future periods.

Forecasting accuracy also does not directly establish economic value or trading profitability.

## 9. Optional simulation extension

The core empirical investigation is complete in scope without simulation experiments.

A separate simulation study could provide additional evidence about the relationship between model specification, mean reversion and estimation uncertainty.

Simulations are particularly useful because the underlying conditional variance is known, unlike in historical market data.

### 9.1 Stationary GARCH-generated returns

The first scenario generates returns from a stationary GARCH(1,1) process:

$$
r_t=\sigma_tz_t,
$$

$$
\sigma_{t+1}^2
=
\omega+\alpha r_t^2+\beta\sigma_t^2,
\qquad
\alpha+\beta<1.
$$

The generating process has a positive long-run variance and genuine mean reversion.

GARCH and EWMA are fitted or calibrated from the simulated historical returns, without supplying the true generating parameters to their estimation procedures.

The experiment examines whether the correctly specified GARCH model produces more accurate forecasts after accounting for finite-sample estimation uncertainty.

### 9.2 EWMA-generated returns

The second scenario uses an integrated variance process:

$$
\sigma_{t+1}^2
=
0.94\sigma_t^2+0.06r_t^2.
$$

This represents a process with EWMA dynamics rather than mean reversion towards a positive long-run variance.

Fitted stationary GARCH is compared with calibrated EWMA.

Because stationary GARCH can approach the integrated boundary, an advantage for EWMA is not assumed.

This scenario also permits investigation of how GARCH estimates behave when the true process lies outside its stationary parameter space.

### 9.3 Simulation evaluation

The simulations use separate estimation and evaluation observations, with repeated independent runs to assess variation in forecasting performance.

The known conditional-variance process permits direct evaluation against

$$
V^*_{t,h}
=
E_t\left[
\sum_{j=1}^{h}\sigma_{t+j}^2
\right],
$$

as well as against realised squared returns.

Differences between these evaluations reveal the influence of noise in the observable variance proxy.

The simulations are intended to clarify model behaviour rather than establish which model is necessarily preferable for historical market data.

## 10. Further possible extensions

Beyond the controlled simulations, several models could address features of volatility not captured by standard Gaussian GARCH(1,1).

| Extension | Motivation |
|---|---|
| **20-day forecasting** | Explore whether mean reversion becomes more relevant over longer horizons |
| **GJR-GARCH** | Investigate asymmetric responses to positive and negative return shocks |
| **Student-t GARCH** | Examine the effect of heavy-tailed innovations |
| **EGARCH** | Represent asymmetric volatility dynamics through log conditional variance |
| **FIGARCH** | Investigate fractional integration and long-memory behaviour |
| **HAR-RV** | Model volatility at multiple time scales, ideally using higher-frequency data |
| **Stochastic volatility** | Treat latent volatility as a stochastic process with its own innovations |
| **Markov-switching volatility** | Investigate changes between distinct volatility regimes |
| **Machine learning** | Compare nonlinear predictive models with traditional statistical specifications |

GJR-GARCH and Student-t GARCH are relatively accessible extensions using the existing return data.

HAR-RV and stochastic-volatility approaches would represent more substantial departures from the initial modelling framework.

These extensions are not part of the core empirical evaluation. Analyses developed after examining the held-out test results would be exploratory unless supported by a new confirmatory evaluation design.

## 11. Research outputs and reproducibility

The core empirical study will produce reproducible Python implementations of the forecasting models, data-processing procedures, automated tests and evaluation methods.

The research report will present the principal out-of-sample comparisons, estimated GARCH parameters, forecast-loss differences, statistical uncertainty and relevant visualisations.

The optional simulation study, if undertaken, will form a separate extension to these results.

The research specification documents the intended methodology before the final test evaluation. Material methodological changes will be recorded in the repository, with prespecified and exploratory analyses distinguished.

The central conclusion will concern **whether the additional complexity of fitted GARCH(1,1) delivers a meaningful improvement over calibrated EWMA, and how the observed performance relates to the estimated volatility dynamics**.

Both positive and inconclusive findings are relevant to this investigation.

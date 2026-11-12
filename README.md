# Consumer Complaint Volume Forecasting Prototype (Week 4, Machine Learning track)

**AnalystLab Africa · Machine Learning Internship · Week 4**
**Author:** Umar Muhammad

Forecasts the number of consumer complaints the CFPB receives about Bank of America each month, using 62,516 complaint records (1 May 2017 - 28 Aug 2023). This is the Machine Learning deliverable of the shared *Consumer Complaint Trends and Response Intelligence Platform* project.

> **Responsible use.** A complaint is a consumer-reported issue; it does not prove misconduct or a regulatory violation. Recorded company responses are not proof of satisfactory resolution. This prototype forecasts complaint *volume* only. It makes no claim about the company's behaviour or future performance.

## Prediction problem
- **Target:** complaints submitted per calendar month (by `Date submitted`), modelled as complaints per weekday and converted back with the target month's weekday count.
- **Horizons:** 1 - 6 months ahead; planning focus 1 - 3 months.
- **Modelling window:** 75 complete months (May 2017 - Jul 2023). **Aug 2023 is partial** (28 days, 20 of 23 weekdays), so it is excluded from training and evaluation and used only as a separate check. May 2017 starts on day 1, so it is a complete month and is kept (a sensitivity test shows no effect).
- **Missing months vs zeros:** no month is missing (76 consecutive); product-months with no complaints are genuine zeros.

## Key findings
- Volume grew about 2.4x between 2018 and 2022; the trend dominates, seasonality is weak.
- Typical 1 - 3 month forecast error is about 8 - 13% of monthly volume (WAPE). Test months Jan - Jul 2023: best model 11.8%, "repeat last month" 13.1%; excluding July 2023: 4.4% vs 5.6%.
- **No method is reliably better than the naive baseline.** The validation winner (Ridge) lost to naive on the test months; no improvement is statistically significant (p >= 0.15); seasonal naive is significantly worse. ARIMA chose a plain random walk at every origin.
- A **burst in July 2023** (1,749 complaints, about 60% above the previous six months' typical level, concentrated on 11 - 15 July) was unpredictable and dominates the test error. Models that carried it forward over-forecast August by more than 120%.
- Planning range for Sep - Oct 2023: roughly 1,100 - 1,500 complaints a month, refreshed monthly.

## Method
1. Data validation and cleaning (blank timely-response = In progress, never "No"; missing sub-issue/public response labelled by meaning; date checks; derived fields).
2. Shared KPI definitions (`docs/KPI_definitions.md`).
3. Trend analysis: monthly series, STL decomposition, product mix, burst investigation.
4. Rolling-origin backtest (expanding window): validation = 2022, test = Jan - Jul 2023; every forecast uses only data up to its origin.
5. Nine methods: naive, seasonal naive, 3-month average, 6-month median, damped exponential smoothing, ARIMA (AIC-selected), ridge regression, gradient boosting, ensemble. Metrics: MAE, RMSE, WAPE.
6. Error analysis, partial-month check (Aug 2023), significance test, sensitivity tests, product-level forecasts, future forecast with rough ranges from backtest errors.

## Repository structure
```
ml-week4/
├── README.md
├── requirements.txt
├── notebook/Complaint_Volume_Forecasting.ipynb   # full analysis, 11 figures
├── src/train_and_forecast.py                     # reproducible re-training from the raw workbook
├── data/
│   ├── raw/        # ORIGINAL workbook and data dictionary (never modified)
│   └── processed/  # monthly series, product series, backtest forecasts/metrics, future forecast
├── models/         # model_recipe.json, complaint_forecaster.joblib
├── reports/        # Complaint_Forecasting_Report (.docx and .pdf), results.json
├── docs/           # DATA_QUALITY.md, KPI_definitions.md, PRESENTATION_SCRIPT.md, CONTRIBUTION_AND_REVISIONS.md, assignment PDF
└── images/         # all figures
```

## How to run
```bash
pip install -r requirements.txt
cd notebook && jupyter notebook Complaint_Volume_Forecasting.ipynb     # full analysis
cd .. && python src/train_and_forecast.py                              # re-train and forecast from the raw workbook
```
`src/train_and_forecast.py` reproduces the notebook's future forecast exactly (checked).

## Assumptions and limitations
- Only 75 monthly points; the late-2018 dip and the July 2023 burst have no explanation in the data, and none is assumed.
- Only complaint counts are used; no external drivers.
- Forecast ranges are rough (about 19 backtest months per horizon); forecasts beyond 3 months are not shown to be reliable.
- The model is re-fitted at each forecast origin, so the "saved model" is the recipe (`models/model_recipe.json`) plus the training script.

## Work plan
The work was planned backwards from the Thursday deadline in four phases so the hardest part (honest validation) was not left to the last day: (1) data audit and KPI definitions, (2) baselines and models, (3) validation, error analysis and sensitivity tests, (4) documentation, report, presentation and posts.

## Data source
Consumer Financial Protection Bureau (CFPB), Consumer Complaints on Financial Products and Services - Bank of America, 2017 - 2023, supplied by AnalystLab Africa.

#AnalystLabAfrica

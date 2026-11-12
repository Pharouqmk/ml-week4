# Individual presentation script (about 7 minutes)

Speak in your own words; these are talking points with approximate timings. Record your screen while showing the notebook and report.

**1. Introduction (0:30)**
Hello, I am Umar Muhammad, on the Machine Learning track. My task was a complaint-volume forecasting prototype for CFPB complaints about Bank of America, 62,516 records from May 2017 to August 2023. Important framing: a complaint is a consumer-reported issue, not proof of misconduct, and my model forecasts how many complaints arrive, nothing about company performance.

**2. Data and validation (1:15)**
- The complaint ID is unique, there are no duplicate rows and no missing months: 76 consecutive months.
- Blank "timely response" values are exactly the 1,494 In-progress complaints, so I did not count them as "No"; they are excluded from the denominator (timely rate 96.06%).
- The forwarding interval is CFPB intake to forwarding, not the company's response time: 79% same day, a few over 30 days.
- August 2023 is a partial month (28 days), so I excluded it from training and testing and used it as an extra check.

**3. What the history shows (1:00)**
- Volume grew about 2.4 times between 2018 and 2022; the trend dominates and seasonality is weak (show Figure 2).
- Two unusual periods: a dip from November 2018 to March 2019, and a burst in July 2023, mostly on 11 to 15 July (show Figure 5). The data do not explain either, so I do not guess a cause.

**4. How I built and tested the models (1:30)**
- Target: complaints per month, modelled per weekday and converted back.
- Nine methods: four baselines, exponential smoothing, ARIMA, ridge, gradient boosting and an ensemble.
- Rolling-origin validation: every forecast uses only data before it. 2022 is validation (tuning and selection), January to July 2023 is the test, used once. This prevents leakage from the future.
- Metrics: MAE, RMSE and WAPE.

**5. Results (1:30)**
- Typical 1 to 3 month error is about 8 to 13% of monthly volume.
- Ridge won validation but lost to the naive "repeat last month" baseline on the test months; gradient boosting was best on test. The ranking changes between periods (show the stability table), and no improvement is statistically significant. ARIMA chose a plain random walk, so it equals the naive baseline.
- The July 2023 burst caused the largest error; models that carried it forward over-forecast August by more than 120%.
- At product level, naive or exponential smoothing won for every product.
- Honest conclusion: on this data, a simple baseline is hard to beat.

**6. Limitations and recommendations (1:00)**
- Short history, unexplained events, no external drivers, rough forecast ranges, not reliable beyond 3 months.
- Recommendations: use forecasts as a planning range (about 1,100 to 1,500 a month for September and October), refresh monthly, keep the naive baseline as a benchmark, monitor daily counts for bursts, and forecast only the larger products.

**7. My contribution and how it supports the team (0:30)**
Fill in honestly, for example: "My forecasting work uses the shared KPI definitions agreed with the team; the monthly series I produced can feed the dashboard's trend page, and my burst finding is useful for the statistics and AI-assistant tracks." Mention only collaboration that really happened.

# Shared KPI definitions (computed from the cleaned data)

| KPI | Definition | Value |
|---|---|---|
| Total complaints | Count of unique Complaint IDs | 62,516 |
| Complaint volume (month / year) | Count of complaints by `Date submitted` (CFPB receipt date) | See `data/processed/monthly_complaints.csv` |
| Annual volume | Same, by calendar year (2017 = May-Dec, 2023 = Jan-28 Aug) | 5,394 / 7,872 / 7,075 / 8,942 / 11,149 / 12,953 / 9,131 (2017-2023) |
| Year-over-year change | (Year N - Year N-1) / Year N-1, complete years only | 2019 -10.1%, 2020 +26.4%, 2021 +24.7%, 2022 +16.2% |
| Product share | Product count / total complaints | Checking or savings 39.7%, Credit/prepaid card 25.9%, Credit reporting 12.3%, Mortgage 10.6%, Money transfer 5.5%, Debt collection 4.4%, others 1.6% |
| Timely-response % | Yes / (Yes + No); In-progress (blank flag) excluded from the denominator | 96.06% (58,619 Yes, 2,403 No) |
| Records excluded from timely-response % | Blank flag, all In progress | 1,494 |
| Complaints In progress | Company response to consumer = In progress | 1,494 |
| Forwarding interval | Date received minus Date submitted (CFPB intake to forwarding; **not** company response time) | Mean 1.22 d, median 0 d |
| Forecast target | Complaints submitted in a calendar month, modelled as complaints per weekday x weekdays in the target month | Complete months May 2017 - Jul 2023 (75) |
| WAPE | Sum of absolute forecast errors / sum of actual values | Reported by horizon and period |

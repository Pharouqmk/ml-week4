# Data-quality documentation

**Dataset:** `data/raw/Consumer_Complaints.xlsx` (sheet `Data`, 62,516 rows x 12 columns), CFPB complaints about Bank of America, 1 May 2017 - 28 Aug 2023. The original file is never modified; all cleaning happens in memory in the notebook (Section 2) and is reproducible.

| # | Check | Result | Decision |
|---|---|---|---|
| 1 | Structure and types | 62,516 x 12; dates are datetimes, all else text/ID | None needed |
| 2 | Complaint ID unique (candidate key) | Yes, 62,516 unique | Used as primary key |
| 3 | Fully duplicated rows | 0 | Nothing removed |
| 4 | Rows identical except ID | 1,494 | Kept: different IDs are different complaints; noted |
| 5 | Missing `Sub-product` | 7 (all checking/savings) | Labelled "Not specified" |
| 6 | Missing `Sub-issue` | 10,858 | Not every issue has a sub-issue; labelled "Not specified" |
| 7 | Missing `Company public response` | 2,175 = 1,494 In progress + 681 closed with none recorded | Labelled "No public response recorded" |
| 8 | Blank `Timely response?` | 1,494, **exactly** the In-progress complaints (crosstab verified) | Labelled "Not yet determined"; **never counted as No**; excluded from the timely-response denominator and reported separately |
| 9 | Date order | 0 complaints with Date received before Date submitted | Valid |
| 10 | Date range | 2017-05-01 to 2023-08-28 (both columns) | Matches the brief |
| 11 | Forwarding interval (Date received - Date submitted) | Mean 1.22 d, median 0 d, 79.4% same day, 435 over 30 d, max 275 d | Kept; flagged as unusually long when >30 days; it is the CFPB intake-to-forwarding interval, not company response time |
| 12 | Whitespace / case variants in text columns | None | None needed |
| 13 | Category oddities | `Submitted via` has "Web Referral" (90) and "Email" (2) alongside "Web"/"Referral"; `Company response to consumer` has "Closed" (8) beside the three "Closed with ..." values | Kept as recorded (meaning not documented); noted |
| 14 | Reporting months | 76 consecutive months, none missing | No gap repair needed |
| 15 | Partial months | Aug 2023 ends on day 28 (20 of 23 weekdays); May 2017 starts on day 1 (complete) | Aug 2023 excluded from modelling and used only as an out-of-sample check; May 2017 kept (sensitivity test shows no effect) |
| 16 | Unusual volume | Dip Nov 2018 - Mar 2019 (as low as 356/month); burst in Jul 2023 (1,749; peak day 12 Jul with 183) | Kept (real data); cause not in the data and not assumed; test accuracy reported with and without July 2023 |
| 17 | Zero-complaint product-months | Student loan 46 months, payday/title/personal loan 3 months | Genuine zeros (every month is covered overall), not missing data |

**Validation after cleaning:** 62,516 rows kept, IDs unique, no missing cells remain, no negative intervals; monthly counts sum to the total.

**Interpretation rules followed:** a complaint is a consumer-reported issue, not proof of misconduct; recorded company responses are not proof of satisfactory resolution; blank timely-response flags are not "No".

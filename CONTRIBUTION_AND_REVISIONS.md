# Individual contribution, collaboration and revisions

The assignment asks for evidence of individual contribution, collaboration and meaningful revisions after feedback. **Only write what really happened.** The sections below are templates; replace every [bracketed] item. Do not leave placeholders in the final submission.

## 1. Individual contribution (what I did myself)
- Validated the CFPB complaint data and documented every cleaning decision (see `docs/DATA_QUALITY.md`).
- Defined the forecasting target, features and rolling-origin validation.
- Built and compared nine forecasting methods; analysed errors; produced product-level and future forecasts.
- Wrote the notebook, training script, report, README and presentation.

## 2. Collaboration with other tracks
[Describe real exchanges only. Examples of what could be true: agreed KPI definitions with the Data Analytics intern; shared the monthly series file `data/processed/monthly_complaints.csv`; gave the July 2023 burst finding to the Data Science and Generative AI interns; checked totals against the dashboard. Add dates, who, and what was agreed.]

| Date | Who | What was shared or agreed | Evidence (message, file, meeting note) |
|---|---|---|---|
| [date] | [name / track] | [description] | [link or screenshot] |

## 3. Feedback received and revisions made
[List actual feedback from mentors or peers and what you changed. If you received none yet, say so, and list the self-review changes below.]

| Date | Feedback / issue found | Change made | Where |
|---|---|---|---|
| [date] | [feedback] | [change] | [file or section] |

### Self-review changes made during development (true for this project)
- Added a 6-month-median baseline and an ensemble after seeing that last-month-based models over-forecast after a burst.
- Added a stability table and significance test after the validation winner lost on the test months, so the conclusion is not overstated.
- Reported test results with and without July 2023 after finding that one burst dominated the error.
- Verified that `src/train_and_forecast.py` reproduces the notebook forecast exactly.

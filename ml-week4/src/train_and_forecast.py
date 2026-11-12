"""Reproducible training workflow for the Consumer Complaint Volume Forecasting prototype.

Reads the ORIGINAL workbook (never modified), rebuilds the monthly series, re-fits the selected model
(Ridge regression on lag/calendar features, forecasting complaints per weekday) and writes forecasts.

Usage (from the project root):
    python src/train_and_forecast.py
    python src/train_and_forecast.py --data data/raw/Consumer_Complaints.xlsx --horizons 3 --out data/processed/forecast_from_script.csv
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

ROOT = Path(__file__).resolve().parents[1]


def weekdays_in_month(p: pd.Period, last_day=None) -> int:
    end = p.end_time.normalize() if last_day is None else min(p.end_time.normalize(), last_day)
    return int((pd.date_range(p.start_time, end).dayofweek < 5).sum())


def build_series(xlsx: Path):
    """Monthly complaint counts by 'Date submitted'; the final month is dropped if it is partial."""
    df = pd.read_excel(xlsx, sheet_name="Data")
    submitted = df["Date submitted"]
    last_day = submitted.max()
    monthly = df.groupby(submitted.dt.to_period("M")).size()
    full_index = pd.period_range(monthly.index.min(), monthly.index.max(), freq="M")
    assert len(full_index) == len(monthly), "a reporting month is missing"
    complete = monthly[[p.end_time.normalize() <= last_day for p in monthly.index]]
    return complete, last_day


def ml_features(r, t, target_month, base_idx=0, h=1):
    return [r[t], r[t - 1], r[t - 2], r[t - 11:t + 1].mean(), r[t - 5:t + 1].mean(), r[t] - r[t - 1],
            np.sin(2 * np.pi * target_month.month / 12), np.cos(2 * np.pi * target_month.month / 12), base_idx + t + h]


def ridge_forecast(series: pd.Series, wd: pd.Series, h: int, alpha: float) -> float:
    target = series.index[-1] + h
    rate = np.log1p((series / wd.loc[series.index]).values.astype(float))
    n = len(rate)
    X, y = [], []
    for t in range(12, n - h):
        X.append(ml_features(rate, t, series.index[t + h], 0, h))
        y.append(rate[t + h])
    X, y = np.array(X), np.array(y)
    xr = np.array([ml_features(rate, n - 1, target, 0, h)])
    mu, sd = X.mean(0), X.std(0) + 1e-9
    pred = Ridge(alpha=alpha).fit((X - mu) / sd, y).predict((xr - mu) / sd)[0]
    return float(np.expm1(pred) * wd.loc[target])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "data/raw/Consumer_Complaints.xlsx"))
    ap.add_argument("--recipe", default=str(ROOT / "models/model_recipe.json"))
    ap.add_argument("--horizons", type=int, default=3)
    ap.add_argument("--out", default=str(ROOT / "data/processed/forecast_from_script.csv"))
    a = ap.parse_args()

    recipe = json.load(open(a.recipe))
    series, last_day = build_series(Path(a.data))
    print(f"Modelling series: {len(series)} complete months, {series.index.min()} to {series.index.max()} (data end {last_day.date()})")

    wd = pd.Series({p: weekdays_in_month(p) for p in pd.period_range(series.index.min(), series.index[-1] + 12, freq="M")})
    q = recipe["interval_ratio_quantiles"]
    rows = []
    for h in range(1, a.horizons + 1):
        tm = series.index[-1] + h
        fc = ridge_forecast(series, wd, h, recipe["ridge_alpha"])
        rate = (series / wd.loc[series.index])
        robust = rate.iloc[-6:].median() * wd.loc[tm]
        lo, hi = q["0.1"][str(h)], q["0.9"][str(h)]
        rows.append({"month": str(tm), "horizon": h, "forecast": round(fc), "low_80": round(fc * lo), "high_80": round(fc * hi),
                     "robust_level_scenario": round(robust), "weekdays": int(wd[tm])})
    out = pd.DataFrame(rows)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(a.out, index=False)
    print(out.to_string(index=False))
    print("Saved:", a.out)


if __name__ == "__main__":
    main()

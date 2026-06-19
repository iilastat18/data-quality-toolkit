from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import DATA_DIR, FIGURES_DIR, REPORTS_DIR, ensure_dirs


plt.style.use("seaborn-v0_8-whitegrid")


EXPECTED_STATUS = {"active", "paused", "closed"}
STALE_CUTOFF = pd.Timestamp("2025-01-01 00:00:00")


def load_data() -> pd.DataFrame:
    path = DATA_DIR / "sample_records.csv"
    if not path.exists():
        raise FileNotFoundError("Sample dataset not found. Run `python src/generate_sample_data.py` first.")
    df = pd.read_csv(path, parse_dates=["snapshot_ts"])
    return df


def zscore_flags(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    clean = series.dropna()
    if clean.empty or clean.std(ddof=0) == 0:
        return pd.Series(False, index=series.index)
    z = (series - clean.mean()) / clean.std(ddof=0)
    return z.abs() > threshold


def build_issue_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    checks: list[dict[str, object]] = []

    duplicate_rows = int(df.duplicated(subset=["record_id", "snapshot_ts"]).sum())
    checks.append({"issue": "duplicate_rows", "count": duplicate_rows, "severity": "high"})

    for column in ["price", "score", "category"]:
        checks.append(
            {
                "issue": f"missing_{column}",
                "count": int(df[column].isna().sum()),
                "severity": "medium",
            }
        )

    negative_qty = int((df["quantity"] < 0).sum())
    checks.append({"issue": "negative_quantity", "count": negative_qty, "severity": "high"})

    stale_rows = int((df["snapshot_ts"] < STALE_CUTOFF).sum())
    checks.append({"issue": "stale_timestamp", "count": stale_rows, "severity": "high"})

    unexpected_status = int((~df["status"].isin(EXPECTED_STATUS)).sum())
    checks.append({"issue": "unexpected_status", "count": unexpected_status, "severity": "medium"})

    price_outliers = int(zscore_flags(df["price"]).sum())
    score_outliers = int(zscore_flags(df["score"]).sum())
    checks.append({"issue": "price_outliers", "count": price_outliers, "severity": "medium"})
    checks.append({"issue": "score_outliers", "count": score_outliers, "severity": "low"})

    summary_df = pd.DataFrame(checks)
    stats = {
        "row_count": int(len(df)),
        "unique_record_ids": int(df["record_id"].nunique()),
        "issues_total": int(summary_df["count"].sum()),
        "high_severity_issues": int(summary_df.loc[summary_df["severity"] == "high", "count"].sum()),
        "rows_with_any_missing": int(df[["price", "score", "category"]].isna().any(axis=1).sum()),
    }
    return summary_df, stats


def save_figures(df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    missing = df.isna().mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    x_positions = np.arange(len(missing))
    ax.bar(x_positions, missing.values, color="#d98d48")
    ax.set_title("Missingness by Column")
    ax.set_ylabel("Percent missing")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(missing.index, rotation=25, ha="right")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "missingness_by_column.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    issue_positions = np.arange(len(summary_df))
    ax.bar(issue_positions, summary_df["count"], color="#1f7763")
    ax.set_title("Issue Breakdown")
    ax.set_ylabel("Count")
    ax.set_xticks(issue_positions)
    ax.set_xticklabels(summary_df["issue"], rotation=35, ha="right")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "issue_breakdown.png", dpi=180)
    plt.close(fig)


def save_report(summary_df: pd.DataFrame, stats: dict[str, object]) -> None:
    report = f"""# Data Quality Report

## Dataset Overview

- Row count: {stats['row_count']}
- Unique record IDs: {stats['unique_record_ids']}
- Total issues counted: {stats['issues_total']}
- High-severity issue count: {stats['high_severity_issues']}
- Rows with at least one missing core field: {stats['rows_with_any_missing']}

## Issue Summary

| Issue | Count | Severity |
| --- | ---: | --- |
"""
    for _, row in summary_df.iterrows():
        report += f"| {row['issue']} | {int(row['count'])} | {row['severity']} |\n"

    report += """

## Interpretation

This synthetic dataset contains a realistic mix of quality problems:

- duplicate rows that would distort downstream reporting
- missing fields that would affect scoring and segmentation
- stale timestamps that suggest delayed ingestion
- invalid statuses that break category assumptions
- outliers that should be reviewed before model or dashboard use

## Portfolio Framing

The purpose of this toolkit is to show how a lightweight validation step can sit between raw data ingestion and downstream analytics or dashboarding.
"""
    (REPORTS_DIR / "data_quality_report.md").write_text(report)


def main() -> None:
    ensure_dirs()
    df = load_data()
    summary_df, stats = build_issue_summary(df)
    summary_df.to_csv(DATA_DIR / "check_summary.csv", index=False)
    save_figures(df, summary_df)
    save_report(summary_df, stats)

    print("Saved outputs:")
    print(f"  - {DATA_DIR / 'check_summary.csv'}")
    print(f"  - {REPORTS_DIR / 'data_quality_report.md'}")
    print(f"  - {FIGURES_DIR / 'missingness_by_column.png'}")
    print(f"  - {FIGURES_DIR / 'issue_breakdown.png'}")


if __name__ == "__main__":
    main()

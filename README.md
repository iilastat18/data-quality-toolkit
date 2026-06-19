<div align="center">
  <h1>Data Quality Toolkit</h1>
  <p><strong>A lightweight validation toolkit for checking missingness, duplicates, stale timestamps, outliers, and category issues.</strong></p>
  <p>Built to show reusable engineering patterns around data reliability and monitoring.</p>
</div>

<p align="center">
  <code>data quality</code>
  <code>validation tooling</code>
  <code>report generation</code>
  <code>monitoring logic</code>
  <code>synthetic sample data</code>
</p>

## Portfolio Role

This is the tooling and reliability repo in the portfolio. It helps balance the more visual projects by showing practical validation logic and report generation.

## Why this project matters

This project complements a dashboard demo and a quant research project by showing a third skill set: tool-building.

It demonstrates how to:

- inspect raw datasets systematically
- define clear validation checks
- generate repeatable quality summaries
- present technical findings in a readable format

## Project Structure

- `data/`: sample raw data and generated summaries
- `figures/`: visualization output
- `reports/`: markdown report produced by the checker
- `src/`: data generation and validation code

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_sample_data.py
python src/run_checks.py
```

## Checks included

- row count and duplicate detection
- missing-value profile by column
- negative and impossible numeric values
- stale timestamp detection
- unexpected category inspection
- simple outlier detection using z-score style thresholds

## Outputs

After running the scripts, you should see:

- `data/sample_records.csv`
- `data/check_summary.csv`
- `reports/data_quality_report.md`
- `figures/missingness_by_column.png`
- `figures/issue_breakdown.png`

## Preview Charts

![Missingness by column](figures/missingness_by_column.png)

![Issue breakdown](figures/issue_breakdown.png)

## Portfolio framing

This is not meant to be a production-grade validation framework. It is a compact, explainable toolkit that shows how I think about data reliability, monitoring, and reusable engineering patterns.

## Screenshot Strategy

- use the issue breakdown chart as the first visual
- optionally include the generated markdown report or summary CSV preview
- frame screenshots around clarity of checks and outputs, not just raw code

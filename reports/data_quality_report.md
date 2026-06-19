# Data Quality Report

## Dataset Overview

- Row count: 494
- Unique record IDs: 480
- Total issues counted: 112
- High-severity issue count: 43
- Rows with at least one missing core field: 55

## Issue Summary

| Issue | Count | Severity |
| --- | ---: | --- |
| duplicate_rows | 14 | high |
| missing_price | 24 | medium |
| missing_score | 19 | medium |
| missing_category | 13 | medium |
| negative_quantity | 9 | high |
| stale_timestamp | 20 | high |
| unexpected_status | 6 | medium |
| price_outliers | 6 | medium |
| score_outliers | 1 | low |


## Interpretation

This synthetic dataset contains a realistic mix of quality problems:

- duplicate rows that would distort downstream reporting
- missing fields that would affect scoring and segmentation
- stale timestamps that suggest delayed ingestion
- invalid statuses that break category assumptions
- outliers that should be reviewed before model or dashboard use

## Portfolio Framing

The purpose of this toolkit is to show how a lightweight validation step can sit between raw data ingestion and downstream analytics or dashboarding.

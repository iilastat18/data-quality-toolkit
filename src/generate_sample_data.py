from __future__ import annotations

import numpy as np
import pandas as pd

from utils import DATA_DIR, ensure_dirs


def build_sample_dataset(seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ensure_dirs()

    n = 480
    categories = ["Core", "Growth", "Income", "Thematic"]
    regions = ["US", "Europe", "Asia"]

    timestamps = pd.date_range("2025-01-02 09:00:00", periods=n, freq="2h")
    df = pd.DataFrame(
        {
            "record_id": [f"REC-{1000 + i}" for i in range(n)],
            "snapshot_ts": timestamps,
            "region": rng.choice(regions, size=n, p=[0.46, 0.34, 0.20]),
            "category": rng.choice(categories, size=n, p=[0.34, 0.29, 0.22, 0.15]),
            "price": np.round(rng.normal(102, 16, size=n), 2),
            "quantity": rng.integers(5, 3500, size=n),
            "score": np.round(rng.normal(72, 11, size=n), 2),
            "status": rng.choice(["active", "paused", "closed"], size=n, p=[0.72, 0.18, 0.10]),
        }
    )

    # Inject realistic quality issues.
    df.loc[rng.choice(df.index, size=24, replace=False), "price"] = np.nan
    df.loc[rng.choice(df.index, size=18, replace=False), "score"] = np.nan
    df.loc[rng.choice(df.index, size=12, replace=False), "category"] = None
    df.loc[rng.choice(df.index, size=8, replace=False), "quantity"] = -rng.integers(1, 40, size=8)
    df.loc[rng.choice(df.index, size=6, replace=False), "status"] = "unknown"
    df.loc[rng.choice(df.index, size=6, replace=False), "price"] = df["price"].median() * 4.8

    stale_idx = rng.choice(df.index, size=20, replace=False)
    df.loc[stale_idx, "snapshot_ts"] = pd.Timestamp("2024-11-15 09:00:00")

    duplicates = df.sample(14, random_state=19).copy()
    duplicates["record_id"] = duplicates["record_id"].values
    df = pd.concat([df, duplicates], ignore_index=True)

    return df


def main() -> None:
    df = build_sample_dataset()
    path = DATA_DIR / "sample_records.csv"
    df.to_csv(path, index=False)
    print(f"Wrote sample dataset to {path}")
    print(df.head())


if __name__ == "__main__":
    main()

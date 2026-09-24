from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "delivery_delays.csv"
OUTPUT = ROOT / "output"

REQUIRED_COLUMNS = {
    "delivery_id",
    "delivery_window",
    "route_type",
    "delay_minutes",
    "package_weight_kg",
}


def load_and_validate() -> pd.DataFrame:
    """Load data and perform required validation checks."""
    deliveries = pd.read_csv(DATA_FILE)

    assert set(deliveries.columns) == REQUIRED_COLUMNS, "Unexpected CSV columns."
    assert deliveries["delivery_id"].notna().all(), "delivery_id cannot be blank."
    assert deliveries["delivery_id"].is_unique, "delivery_id values must be unique."

    return deliveries


def write_starter_profile(deliveries: pd.DataFrame) -> None:
    """Create starter profile."""
    profile = pd.DataFrame(
        {
            "column": deliveries.columns,
            "rows": len(deliveries),
            "missing_values": [
                int(deliveries[col].isna().sum())
                for col in deliveries.columns
            ],
            "distinct_values": [
                int(deliveries[col].nunique(dropna=True))
                for col in deliveries.columns
            ],
        }
    )

    profile.to_csv(
        OUTPUT / "starter_profile.csv",
        index=False
    )


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)

    deliveries = load_and_validate()

    write_starter_profile(deliveries)

    print(f"Dataset grain: one row = one completed delivery stop")
    print(f"Total records: {len(deliveries)}")

    # Step 1
    deliveries["delay_minutes"] = pd.to
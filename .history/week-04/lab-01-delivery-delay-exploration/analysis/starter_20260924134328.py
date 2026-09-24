from pathlib import Path

import pandas as pd


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
    """Load the authorized fictional data and complete basic integrity checks."""
    deliveries = pd.read_csv(DATA_FILE)
    assert set(deliveries.columns) == REQUIRED_COLUMNS, "Unexpected CSV columns."
    assert deliveries["delivery_id"].notna().all(), "delivery_id cannot be blank."
    assert deliveries["delivery_id"].is_unique, "delivery_id values must be unique."
    return deliveries


def write_starter_profile(deliveries: pd.DataFrame) -> None:
    """Create starter evidence only; this is not the completed lab analysis."""
    profile = pd.DataFrame({
        "column": deliveries.columns,
        "rows": len(deliveries),
        "missing_values": [int(deliveries[column].isna().sum()) for column in deliveries.columns],
        "distinct_values": [int(deliveries[column].nunique(dropna=True)) for column in deliveries.columns],
    })
    profile.to_csv(OUTPUT / "starter_profile.csv", index=False)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    deliveries = load_and_validate()
    write_starter_profile(deliveries)
    print(f"Starter checks passed for {len(deliveries)} fictional delivery-stop records.")
    print("Created output/starter_profile.csv.")
    print("Next: complete the guided delay analysis and one independent univariate analysis.")

    # Your Step 1: Convert delay_minutes to numeric and identify missing values.
    # Your Step 2: Create the required delay summary and save it as CSV.
    # Your Step 3: Calculate an IQR fence and save possible high-delay records.
    # Your Step 4: Create the required labelled delay histogram and box plot.
    # Your Step 5: Complete one independent univariate analysis.
    # Do not hard-code results. Calculate every value from delivery_delays.csv.


if __name__ == "__main__":
    main()

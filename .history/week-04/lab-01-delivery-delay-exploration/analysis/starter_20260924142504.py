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
    deliveries = pd.read_csv(DATA_FILE)

    assert set(deliveries.columns) == REQUIRED_COLUMNS, "Unexpected CSV columns."
    assert deliveries["delivery_id"].notna().all(), "delivery_id cannot be blank."
    assert deliveries["delivery_id"].is_unique, "delivery_id values must be unique."

    return deliveries


def write_starter_profile(deliveries: pd.DataFrame) -> None:
    profile = pd.DataFrame(
        {
            "column": deliveries.columns,
            "rows": len(deliveries),
            "missing_values": [
                int(deliveries[column].isna().sum())
                for column in deliveries.columns
            ],
            "distinct_values": [
                int(deliveries[column].nunique(dropna=True))
                for column in deliveries.columns
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

    print("Dataset grain: one row = one completed delivery stop")
    print(f"Total records: {len(deliveries)}")

    # Step 1
    deliveries["delay_minutes"] = pd.to_numeric(
        deliveries["delay_minutes"],
        errors="coerce"
    )

    missing_values = deliveries["delay_minutes"].isna().sum()

    print(f"Missing delay values: {missing_values}")

    # Step 2
    usable_delays = deliveries["delay_minutes"].dropna()

    q1 = usable_delays.quantile(0.25)
    q3 = usable_delays.quantile(0.75)
    iqr = q3 - q1

    delay_summary = pd.DataFrame(
        {
            "Metric": [
                "Usable Row Count",
                "Mean",
                "Median",
                "Minimum",
                "Maximum",
                "Q1",
                "Q3",
                "IQR",
            ],
            "Value": [
                len(usable_delays),
                usable_delays.mean(),
                usable_delays.median(),
                usable_delays.min(),
                usable_delays.max(),
                q1,
                q3,
                iqr,
            ],
        }
    )

    delay_summary.to_csv(
        OUTPUT / "delay_summary.csv",
        index=False
    )

    print("Created delay_summary.csv")

    # Step 3
    upper_fence = q3 + (1.5 * iqr)

    possible_high_delays = deliveries[
        deliveries["delay_minutes"] > upper_fence
    ]

    possible_high_delays.to_csv(
        OUTPUT / "possible_high_delays.csv",
        index=False
    )

    print("Created possible_high_delays.csv")

    # Step 4 - Combined chart
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(
        usable_delays,
        bins=10,
        edgecolor="black"
    )
    axes[0].set_title("Delivery Delay Histogram")
    axes[0].set_xlabel("Delay Minutes")
    axes[0].set_ylabel("Frequency")

    axes[1].boxplot(
        usable_delays,
        orientation="vertical"
    )
    axes[1].set_title("Delivery Delay Box Plot")
    axes[1].set_ylabel("Delay Minutes")

    plt.tight_layout()
    plt.savefig(OUTPUT / "delay_charts.png")
    plt.close()

    print("Created delay_charts.png")

    # Step 5 - Independent Analysis
    package_summary = deliveries["package_weight_kg"].describe()

    package_summary.to_csv(
        OUTPUT / "package_weight_summary.csv",
        header=["Value"]
    )

    plt.figure(figsize=(8, 5))

    deliveries["package_weight_kg"].hist(
        bins=10,
        edgecolor="black"
    )

    plt.title("Package Weight Distribution")
    plt.xlabel("Package Weight (kg)")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(
        OUTPUT / "package_weight_histogram.png"
    )
    plt.close()

    print("Created package_weight_summary.csv")
    print("Created package_weight_histogram.png")

    print("Lab analysis complete.")


if __name__ == "__main__":
    main()
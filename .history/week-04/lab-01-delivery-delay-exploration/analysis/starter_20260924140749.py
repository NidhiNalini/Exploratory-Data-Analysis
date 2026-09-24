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

    profile.to_csv(OUTPUT / "starter_profile.csv", index=False)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)

    deliveries = load_and_validate()

    write_starter_profile(deliveries)

    print(
        f"Starter checks passed for {len(deliveries)} fictional delivery-stop records."
    )
    print("Created output/starter_profile.csv.")

    # STEP 1
    deliveries["delay_minutes"] = pd.to_numeric(
        deliveries["delay_minutes"],
        errors="coerce"
    )

    missing_delays = deliveries["delay_minutes"].isna().sum()

    print(f"Missing delay values: {missing_delays}")

    # STEP 2
    delay_summary = deliveries["delay_minutes"].describe()

    delay_summary.to_csv(
        OUTPUT / "delay_summary.csv",
        header=["value"]
    )

    print("Created delay_summary.csv")

    # STEP 3
    q1 = deliveries["delay_minutes"].quantile(0.25)
    q3 = deliveries["delay_minutes"].quantile(0.75)

    iqr = q3 - q1

    upper_fence = q3 + (1.5 * iqr)

    high_delay_records = deliveries[
        deliveries["delay_minutes"] > upper_fence
    ]

    high_delay_records.to_csv(
        OUTPUT / "high_delay_records.csv",
        index=False
    )

    print("Created high_delay_records.csv")

    # STEP 4 Histogram
    plt.figure(figsize=(8, 5))
    deliveries["delay_minutes"].dropna().hist(
        bins=10,
        edgecolor="black"
    )

    plt.title("Distribution of Delivery Delays")
    plt.xlabel("Delay Minutes")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(OUTPUT / "delay_histogram.png")
    plt.close()

    # STEP 4 Box Plot
    plt.figure(figsize=(8, 5))

    plt.boxplot(
        deliveries["delay_minutes"].dropna(),
        vert=True
    )

    plt.title("Delivery Delay Box Plot")
    plt.ylabel("Delay Minutes")

    plt.tight_layout()
    plt.savefig(OUTPUT / "delay_boxplot.png")
    plt.close()

    print("Created delay_histogram.png")
    print("Created delay_boxplot.png")

    # STEP 5 Independent Univariate Analysis
    package_summary = deliveries["package_weight_kg"].describe()

    package_summary.to_csv(
        OUTPUT / "package_weight_summary.csv",
        header=["value"]
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
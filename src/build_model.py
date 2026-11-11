"""Build campaign reporting tables from the UCI Bank Marketing data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = {
    "age", "job", "marital", "education", "default", "balance",
    "housing", "loan", "contact", "day", "month", "duration",
    "campaign", "pdays", "previous", "poutcome", "y",
}
MONTH_ORDER = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def load_contacts(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, sep=";")
    missing = sorted(EXPECTED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")
    if not frame["y"].isin(["yes", "no"]).all():
        raise ValueError("Target y must contain only yes and no.")
    invalid_months = sorted({
        str(value) for value in frame["month"].dropna() if value not in MONTH_ORDER
    })
    if frame["month"].isna().any() or invalid_months:
        raise ValueError(f"Invalid month values: {invalid_months}")

    frame = frame.copy()
    frame.insert(0, "contact_id", range(1, len(frame) + 1))
    frame["converted"] = frame["y"].eq("yes").astype(int)
    frame["prior_contacted"] = frame["pdays"].ne(-1)
    frame["contact_attempt_band"] = pd.cut(
        frame["campaign"],
        bins=[0, 1, 2, 3, 5, float("inf")],
        labels=["1", "2", "3", "4-5", "6+"],
        right=True,
    )
    frame["age_band"] = pd.cut(
        frame["age"],
        bins=[17, 29, 39, 49, 59, float("inf")],
        labels=["18-29", "30-39", "40-49", "50-59", "60+"],
    )
    frame["duration_band"] = pd.cut(
        frame["duration"],
        bins=[-1, 60, 180, 300, 600, float("inf")],
        labels=["0-60s", "61-180s", "181-300s", "301-600s", "600s+"],
    )
    frame["month_number"] = frame["month"].map(
        {month: number for number, month in enumerate(MONTH_ORDER, start=1)}
    )
    return frame


def summarize(frame: pd.DataFrame, dimensions: list[str]) -> pd.DataFrame:
    result = (
        frame.groupby(dimensions, dropna=False, observed=True)
        .agg(
            contacts=("contact_id", "count"),
            conversions=("converted", "sum"),
            average_attempts=("campaign", "mean"),
            average_balance=("balance", "mean"),
        )
        .reset_index()
    )
    result["conversion_rate"] = result["conversions"] / result["contacts"]
    return result


def build_model(source: Path, output_dir: Path) -> None:
    contacts = load_contacts(source)
    output_dir.mkdir(parents=True, exist_ok=True)

    tables = {
        "fact_campaign_contacts.csv": contacts,
        "segment_performance.csv": summarize(
            contacts, ["job", "age_band", "education"]
        ),
        "channel_performance.csv": summarize(contacts, ["contact"]),
        "monthly_performance.csv": summarize(
            contacts, ["month_number", "month"]
        ).sort_values("month_number"),
        "contact_frequency_performance.csv": summarize(
            contacts, ["contact_attempt_band"]
        ),
        "prior_outcome_performance.csv": summarize(contacts, ["poutcome"]),
    }
    for filename, table in tables.items():
        table.to_csv(output_dir / filename, index=False)

    print(f"Wrote {len(tables)} campaign reporting tables to {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build campaign BI tables.")
    parser.add_argument(
        "--source", type=Path, default=Path("data/raw/bank-full.csv")
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/processed")
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    build_model(arguments.source, arguments.output_dir)

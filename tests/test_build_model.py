"""Bank Marketing CSV validation regressions."""

import pandas as pd
import pytest

from src.build_model import EXPECTED_COLUMNS, load_contacts


def source_csv(tmp_path, **overrides):
    row = {column: "unknown" for column in EXPECTED_COLUMNS}
    row.update({
        "age": 30, "balance": 100, "day": 1, "month": "jan",
        "duration": 120, "campaign": 1, "pdays": -1, "previous": 0,
        "y": "yes",
    })
    row.update(overrides)
    path = tmp_path / "bank.csv"
    pd.DataFrame([row]).to_csv(path, sep=";", index=False)
    return path


def test_valid_month_maps_to_calendar_order(tmp_path):
    result = load_contacts(source_csv(tmp_path, month="dec"))
    assert result["month_number"].iloc[0] == 12
    assert result["converted"].iloc[0] == 1


@pytest.mark.parametrize("month", ["not-a-month", None])
def test_invalid_month_fails_instead_of_becoming_missing_kpi(tmp_path, month):
    with pytest.raises(ValueError, match="Invalid month values"):
        load_contacts(source_csv(tmp_path, month=month))


@pytest.mark.parametrize(
    "field,value",
    [("campaign", 0), ("campaign", "bad"), ("age", 17), ("duration", -1)],
)
def test_invalid_numeric_inputs_fail_before_banding(tmp_path, field, value):
    with pytest.raises(ValueError, match=f"{field} must be finite"):
        load_contacts(source_csv(tmp_path, **{field: value}))


def test_zero_duration_is_a_valid_completed_contact(tmp_path):
    result = load_contacts(source_csv(tmp_path, duration=0))
    assert result["duration_band"].iloc[0] == "0-60s"

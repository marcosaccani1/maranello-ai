"""Validate the synthetic Maranello AI manufacturing dataset."""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


DATASET_FILE = (
    Path(__file__).parent / "manufacturing_quality_data.csv"
)

EXPECTED_ROWS = 2000
EXPECTED_COLUMNS = 20

EXPECTED_COLUMN_NAMES = (
    "batch_id",
    "production_date",
    "plant",
    "production_line",
    "vehicle_model",
    "shift",
    "units_produced",
    "defective_units",
    "defect_category",
    "rework_units",
    "scrap_units",
    "downtime_minutes",
    "cycle_time_seconds",
    "quality_score",
    "supplier_id",
    "component_category",
    "inspection_status",
    "temperature_c",
    "operator_team",
    "notes",
)

VALID_DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m-%d-%Y",
)


def load_dataset() -> list[dict[str, str]]:
    """Load the dataset from disk."""
    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    with DATASET_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        if tuple(reader.fieldnames or ()) != EXPECTED_COLUMN_NAMES:
            raise ValueError("Dataset schema does not match expectations")

        return list(reader)


def count_exact_duplicates(
    records: list[dict[str, str]],
) -> int:
    """Count exact duplicate rows."""
    serialized_rows = [
        tuple(record[column] for column in EXPECTED_COLUMN_NAMES)
        for record in records
    ]

    frequencies = Counter(serialized_rows)

    return sum(
        count - 1
        for count in frequencies.values()
        if count > 1
    )


def count_missing_values(
    records: list[dict[str, str]],
) -> dict[str, int]:
    """Count empty values for every dataset column."""
    return {
        column: sum(
            1
            for record in records
            if not record[column].strip()
        )
        for column in EXPECTED_COLUMN_NAMES
    }


def detect_date_formats(
    records: list[dict[str, str]],
) -> Counter[str]:
    """Detect the date representations used in the dataset."""
    detected_formats: Counter[str] = Counter()

    for record in records:
        raw_date = record["production_date"]

        matched_format = None

        for date_format in VALID_DATE_FORMATS:
            try:
                datetime.strptime(raw_date, date_format)
            except ValueError:
                continue

            matched_format = date_format
            break

        if matched_format is None:
            detected_formats["invalid"] += 1
        else:
            detected_formats[matched_format] += 1

    return detected_formats


def count_invalid_quality_scores(
    records: list[dict[str, str]],
) -> int:
    """Count quality scores outside the valid 0-100 range."""
    invalid_count = 0

    for record in records:
        value = record["quality_score"].strip()

        if not value:
            continue

        quality_score = float(value)

        if not 0 <= quality_score <= 100:
            invalid_count += 1

    return invalid_count


def count_invalid_defect_relationships(
    records: list[dict[str, str]],
) -> int:
    """Count records where defects exceed produced units."""
    return sum(
        1
        for record in records
        if int(record["defective_units"])
        > int(record["units_produced"])
    )


def count_downtime_outliers(
    records: list[dict[str, str]],
) -> int:
    """Count intentionally extreme downtime observations."""
    count = 0

    for record in records:
        value = record["downtime_minutes"].strip()

        if value and float(value) >= 600:
            count += 1

    return count


def count_cycle_time_outliers(
    records: list[dict[str, str]],
) -> int:
    """Count intentionally extreme cycle-time observations."""
    return sum(
        1
        for record in records
        if float(record["cycle_time_seconds"]) >= 400
    )


def count_dirty_shift_values(
    records: list[dict[str, str]],
) -> int:
    """Count shift values requiring normalization."""
    valid_values = {
        "Morning",
        "Afternoon",
        "Night",
    }

    return sum(
        1
        for record in records
        if record["shift"] not in valid_values
    )


def count_dirty_line_values(
    records: list[dict[str, str]],
) -> int:
    """Count production-line values containing extra whitespace."""
    return sum(
        1
        for record in records
        if record["production_line"]
        != record["production_line"].strip()
    )


def count_dirty_supplier_values(
    records: list[dict[str, str]],
) -> int:
    """Count supplier identifiers containing extra whitespace."""
    return sum(
        1
        for record in records
        if record["supplier_id"]
        and record["supplier_id"]
        != record["supplier_id"].strip()
    )


def validate_dataset(records: list[dict[str, str]]) -> dict[str, Any]:
    """Run validation checks and return their results."""
    missing_values = count_missing_values(records)
    date_formats = detect_date_formats(records)

    results = {
        "rows": len(records),
        "columns": len(EXPECTED_COLUMN_NAMES),
        "duplicates": count_exact_duplicates(records),
        "missing_quality_score": missing_values["quality_score"],
        "missing_supplier_id": missing_values["supplier_id"],
        "missing_downtime": missing_values["downtime_minutes"],
        "date_formats": dict(date_formats),
        "invalid_quality_scores": count_invalid_quality_scores(
            records
        ),
        "invalid_defect_relationships": (
            count_invalid_defect_relationships(records)
        ),
        "downtime_outliers": count_downtime_outliers(records),
        "cycle_time_outliers": count_cycle_time_outliers(records),
        "dirty_shift_values": count_dirty_shift_values(records),
        "dirty_line_values": count_dirty_line_values(records),
        "dirty_supplier_values": count_dirty_supplier_values(records),
    }

    assert results["rows"] == EXPECTED_ROWS
    assert results["columns"] == EXPECTED_COLUMNS

    assert results["duplicates"] >= 20

    assert results["missing_quality_score"] > 0
    assert results["missing_supplier_id"] > 0
    assert results["missing_downtime"] > 0

    assert len(results["date_formats"]) >= 3

    assert results["invalid_quality_scores"] > 0
    assert results["invalid_defect_relationships"] > 0

    assert results["downtime_outliers"] > 0
    assert results["cycle_time_outliers"] > 0

    assert results["dirty_shift_values"] > 0
    assert results["dirty_line_values"] > 0
    assert results["dirty_supplier_values"] > 0

    return results


def print_results(results: dict[str, Any]) -> None:
    """Print the dataset validation report."""
    print("Maranello AI Dataset Validation")
    print("=" * 40)

    for name, value in results.items():
        print(f"{name}: {value}")

    print("=" * 40)
    print("Dataset validation passed successfully.")


def main() -> None:
    """Load and validate the generated dataset."""
    records = load_dataset()
    results = validate_dataset(records)
    print_results(results)


if __name__ == "__main__":
    main()
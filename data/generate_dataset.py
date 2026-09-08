"""Generate the synthetic Maranello AI manufacturing quality dataset."""

from __future__ import annotations

import csv
import random
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path
from typing import Any


RANDOM_SEED = 42

UNIQUE_RECORDS = 1980
DUPLICATE_RECORDS = 20

OUTPUT_FILE = Path(__file__).parent / "manufacturing_quality_data.csv"

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)

PLANTS = (
    "Plant 01",
    "Plant 02",
)

PRODUCTION_LINES = (
    "Line 1",
    "Line 2",
    "Line 3",
    "Line 4",
)

VEHICLE_MODELS = (
    "Aquila GT",
    "Veloce S",
    "Strada X",
    "Eterna",
)

SHIFTS = (
    "Morning",
    "Afternoon",
    "Night",
)

DEFECT_CATEGORIES = (
    "Paint",
    "Assembly",
    "Electronics",
    "Mechanical",
    "Interior",
    "Dimensional",
)

SUPPLIERS = tuple(f"SUP-{number:02d}" for number in range(1, 13))

COMPONENT_CATEGORIES = (
    "Body",
    "Powertrain",
    "Electronics",
    "Interior",
    "Braking",
    "Suspension",
)

OPERATOR_TEAMS = (
    "Team Alpha",
    "Team Beta",
    "Team Gamma",
    "Team Delta",
)

NOTES = (
    "",
    "",
    "",
    "",
    "Routine quality inspection completed.",
    "Minor process adjustment performed.",
    "Supplier component verification required.",
    "Production line calibration completed.",
)


def random_date() -> date:
    """Return a random production date within the configured period."""
    total_days = (END_DATE - START_DATE).days

    return START_DATE + timedelta(days=random.randint(0, total_days))


def random_binomial(trials: int, probability: float) -> int:
    """Generate a binomial-like result using deterministic random sampling."""
    return sum(
        1
        for _ in range(trials)
        if random.random() < probability
    )


def calculate_defect_probability(
    production_line: str,
    shift: str,
    supplier_id: str,
    component_category: str,
) -> float:
    """Calculate a realistic defect probability using operational factors."""
    probability = 0.015

    if production_line == "Line 3":
        probability += 0.008

    if shift == "Night":
        probability += 0.005

    if supplier_id == "SUP-07":
        probability += 0.010

    if component_category == "Electronics":
        probability += 0.006

    return min(probability, 0.08)


def determine_inspection_status(
    defect_rate: float,
    quality_score: float,
) -> str:
    """Determine the quality inspection outcome."""
    if defect_rate > 0.04 or quality_score < 88:
        return "Failed"

    if defect_rate > 0.025 or quality_score < 94:
        return "Review"

    return "Passed"


def generate_record(index: int) -> dict[str, Any]:
    """Generate a single clean manufacturing batch record."""
    production_line = random.choice(PRODUCTION_LINES)
    vehicle_model = random.choice(VEHICLE_MODELS)
    shift = random.choice(SHIFTS)
    supplier_id = random.choice(SUPPLIERS)
    component_category = random.choice(COMPONENT_CATEGORIES)

    units_produced = random.randint(45, 120)

    defect_probability = calculate_defect_probability(
        production_line=production_line,
        shift=shift,
        supplier_id=supplier_id,
        component_category=component_category,
    )

    defective_units = random_binomial(
        units_produced,
        defect_probability,
    )

    rework_units = (
        random.randint(0, defective_units)
        if defective_units
        else 0
    )

    remaining_defects = max(defective_units - rework_units, 0)

    scrap_units = (
        random.randint(0, remaining_defects)
        if remaining_defects
        else 0
    )

    downtime_minutes = max(
        0.0,
        random.gauss(28, 17),
    )

    if production_line == "Line 3":
        downtime_minutes += random.uniform(3, 10)

    cycle_time_seconds = max(
        40.0,
        random.gauss(82, 9),
    )

    if shift == "Night":
        cycle_time_seconds += random.uniform(1, 5)

    defect_rate = (
        defective_units / units_produced
        if units_produced
        else 0
    )

    quality_score = (
        99
        - defect_rate * 120
        - downtime_minutes * 0.025
        + random.gauss(0, 1.2)
    )

    quality_score = round(
        min(max(quality_score, 70), 100),
        2,
    )

    inspection_status = determine_inspection_status(
        defect_rate=defect_rate,
        quality_score=quality_score,
    )

    defect_category = (
        random.choice(DEFECT_CATEGORIES)
        if defective_units > 0
        else "None"
    )

    temperature_c = round(
        random.gauss(22.5, 2.2),
        1,
    )

    return {
        "batch_id": f"BATCH-{index:05d}",
        "production_date": random_date().isoformat(),
        "plant": random.choice(PLANTS),
        "production_line": production_line,
        "vehicle_model": vehicle_model,
        "shift": shift,
        "units_produced": units_produced,
        "defective_units": defective_units,
        "defect_category": defect_category,
        "rework_units": rework_units,
        "scrap_units": scrap_units,
        "downtime_minutes": round(downtime_minutes, 2),
        "cycle_time_seconds": round(cycle_time_seconds, 2),
        "quality_score": quality_score,
        "supplier_id": supplier_id,
        "component_category": component_category,
        "inspection_status": inspection_status,
        "temperature_c": temperature_c,
        "operator_team": random.choice(OPERATOR_TEAMS),
        "notes": random.choice(NOTES),
    }


def select_unique_indices(
    total_records: int,
    count: int,
) -> list[int]:
    """Return a deterministic sample of unique record indices."""
    return random.sample(range(total_records), count)


def inject_missing_values(records: list[dict[str, Any]]) -> None:
    """Inject controlled missing values."""
    for index in select_unique_indices(len(records), 20):
        records[index]["quality_score"] = ""

    for index in select_unique_indices(len(records), 15):
        records[index]["supplier_id"] = ""

    for index in select_unique_indices(len(records), 20):
        records[index]["downtime_minutes"] = ""


def inject_category_inconsistencies(
    records: list[dict[str, Any]],
) -> None:
    """Inject inconsistent categorical formatting."""
    shift_variants = (
        "night",
        "NIGHT",
        " Night ",
    )

    for index in select_unique_indices(len(records), 12):
        records[index]["shift"] = random.choice(shift_variants)

    for index in select_unique_indices(len(records), 10):
        line = records[index]["production_line"]
        records[index]["production_line"] = f" {line} "


def inject_date_inconsistencies(
    records: list[dict[str, Any]],
) -> None:
    """Inject alternative date representations."""
    indices = select_unique_indices(len(records), 12)

    for position, index in enumerate(indices):
        original_date = date.fromisoformat(
            records[index]["production_date"]
        )

        if position % 2 == 0:
            records[index]["production_date"] = (
                original_date.strftime("%d/%m/%Y")
            )
        else:
            records[index]["production_date"] = (
                original_date.strftime("%m-%d-%Y")
            )


def inject_invalid_values(
    records: list[dict[str, Any]],
) -> None:
    """Inject values violating expected business constraints."""
    for index in select_unique_indices(len(records), 6):
        records[index]["quality_score"] = round(
            random.uniform(101, 115),
            2,
        )

    for index in select_unique_indices(len(records), 6):
        units_produced = records[index]["units_produced"]

        records[index]["defective_units"] = (
            units_produced + random.randint(1, 10)
        )


def inject_outliers(
    records: list[dict[str, Any]],
) -> None:
    """Inject controlled numerical outliers."""
    for index in select_unique_indices(len(records), 8):
        records[index]["downtime_minutes"] = round(
            random.uniform(600, 900),
            2,
        )

    for index in select_unique_indices(len(records), 8):
        records[index]["cycle_time_seconds"] = round(
            random.uniform(400, 700),
            2,
        )


def inject_supplier_whitespace(
    records: list[dict[str, Any]],
) -> None:
    """Inject supplier identifiers containing extra whitespace."""
    for index in select_unique_indices(len(records), 10):
        supplier_id = records[index]["supplier_id"]

        if supplier_id:
            records[index]["supplier_id"] = f"{supplier_id} "


def add_duplicate_records(
    records: list[dict[str, Any]],
) -> None:
    """Append exact duplicate records to the dataset."""
    duplicate_indices = select_unique_indices(
        len(records),
        DUPLICATE_RECORDS,
    )

    duplicates = [
        deepcopy(records[index])
        for index in duplicate_indices
    ]

    records.extend(duplicates)


def inject_anomalies(records: list[dict[str, Any]]) -> None:
    """Inject all controlled data-quality anomalies."""
    inject_missing_values(records)
    inject_category_inconsistencies(records)
    inject_date_inconsistencies(records)
    inject_invalid_values(records)
    inject_outliers(records)
    inject_supplier_whitespace(records)


def write_dataset(records: list[dict[str, Any]]) -> None:
    """Write generated records to the configured CSV file."""
    if not records:
        raise ValueError("Cannot write an empty dataset")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys(),
        )

        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    """Generate and persist the complete synthetic dataset."""
    random.seed(RANDOM_SEED)

    records = [
        generate_record(index)
        for index in range(1, UNIQUE_RECORDS + 1)
    ]

    inject_anomalies(records)
    add_duplicate_records(records)

    random.shuffle(records)

    write_dataset(records)

    print(
        f"Dataset generated successfully: {OUTPUT_FILE}"
    )
    print(f"Rows generated: {len(records)}")
    print(f"Random seed: {RANDOM_SEED}")


if __name__ == "__main__":
    main()
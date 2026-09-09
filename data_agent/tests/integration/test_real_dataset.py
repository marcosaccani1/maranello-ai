import pandas as pd

from app.core.config import settings
from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader

EXPECTED_COLUMNS = [
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
]


def test_real_manufacturing_dataset_can_be_loaded() -> None:
    loader = DataLoader(settings.dataset_path)

    dataframe = loader.load()

    assert dataframe.shape == (2000, 20)
    assert list(dataframe.columns) == EXPECTED_COLUMNS


def test_real_dataset_contains_expected_dirty_data() -> None:
    loader = DataLoader(settings.dataset_path)

    dataframe = loader.load()

    assert dataframe.duplicated().sum() > 0
    assert dataframe["quality_score"].isna().sum() > 0
    assert dataframe["supplier_id"].isna().sum() > 0
    assert dataframe["downtime_minutes"].isna().sum() > 0


def test_real_dataset_cleaning_removes_duplicates() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()

    dataframe = loader.load()
    cleaned = cleaner.clean(dataframe)

    assert len(dataframe) == 2000
    assert dataframe.duplicated().sum() == 20

    assert len(cleaned) == 1980
    assert cleaned.duplicated().sum() == 0


def test_real_dataset_cleaning_normalizes_categories() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()

    dataframe = loader.load()
    cleaned = cleaner.clean(dataframe)

    assert set(cleaned["shift"].dropna().unique()) == {
        "Morning",
        "Afternoon",
        "Night",
    }

    assert cleaned["production_line"].str.strip().equals(
        cleaned["production_line"]
    )

    supplier_ids = cleaned["supplier_id"].dropna()

    assert supplier_ids.str.strip().equals(supplier_ids)


def test_real_dataset_cleaning_normalizes_dates() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()

    cleaned = cleaner.clean(loader.load())

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["production_date"]
    )
    assert cleaned["production_date"].notna().all()


def test_real_dataset_cleaning_invalidates_impossible_quality_scores() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()

    dataframe = loader.load()
    cleaned = cleaner.clean(dataframe)

    assert (dataframe["quality_score"] > 100).sum() > 0
    assert (cleaned["quality_score"].dropna() > 100).sum() == 0


def test_real_dataset_cleaning_preserves_operational_outliers() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()

    cleaned = cleaner.clean(loader.load())

    assert (cleaned["downtime_minutes"] >= 600).any()
    assert (cleaned["cycle_time_seconds"] >= 400).any()


def test_real_dataset_cleaning_flags_invalid_defect_records() -> None:
    loader = DataLoader(settings.dataset_path)
    cleaner = DataCleaner()

    dataframe = loader.load()
    cleaned = cleaner.clean(dataframe)

    raw_invalid_records = (
        dataframe["defective_units"] > dataframe["units_produced"]
    ).sum()

    assert raw_invalid_records > 0

    assert (
        cleaned.loc[
            ~cleaned["valid_defect_data"],
            "defective_units",
        ]
        > cleaned.loc[
            ~cleaned["valid_defect_data"],
            "units_produced",
        ]
    ).any()

    assert cleaned["valid_defect_data"].dtype == bool
import pandas as pd

from app.services.data_cleaner import DataCleaner


def test_clean_removes_exact_duplicates() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001", "BATCH-001"],
            "production_date": ["2025-01-01", "2025-01-01"],
            "production_line": ["Line 1", "Line 1"],
            "shift": ["Morning", "Morning"],
            "supplier_id": ["SUP-01", "SUP-01"],
            "quality_score": [95.0, 95.0],
            "units_produced": [100, 100],
            "defective_units": [3, 3],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert len(cleaned) == 1


def test_clean_normalizes_text_fields() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001"],
            "production_date": ["2025-01-01"],
            "production_line": [" Line 3 "],
            "shift": [" NIGHT "],
            "supplier_id": [" SUP-07 "],
            "quality_score": [95.0],
            "units_produced": [100],
            "defective_units": [3],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert cleaned.loc[0, "production_line"] == "Line 3"
    assert cleaned.loc[0, "shift"] == "Night"
    assert cleaned.loc[0, "supplier_id"] == "SUP-07"


def test_clean_normalizes_mixed_date_formats() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001", "BATCH-002", "BATCH-003"],
            "production_date": [
                "2025-01-15",
                "15/01/2025",
                "01-15-2025",
            ],
            "production_line": ["Line 1", "Line 1", "Line 1"],
            "shift": ["Morning", "Morning", "Morning"],
            "supplier_id": ["SUP-01", "SUP-01", "SUP-01"],
            "quality_score": [95.0, 95.0, 95.0],
            "units_produced": [100, 100, 100],
            "defective_units": [3, 3, 3],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert pd.api.types.is_datetime64_any_dtype(cleaned["production_date"])
    assert cleaned["production_date"].notna().all()

    expected_date = pd.Timestamp("2025-01-15")

    assert (cleaned["production_date"] == expected_date).all()


def test_clean_invalidates_quality_score_above_100() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001", "BATCH-002"],
            "production_date": ["2025-01-01", "2025-01-02"],
            "production_line": ["Line 1", "Line 2"],
            "shift": ["Morning", "Afternoon"],
            "supplier_id": ["SUP-01", "SUP-02"],
            "quality_score": [95.0, 105.0],
            "units_produced": [100, 100],
            "defective_units": [3, 3],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert cleaned.loc[0, "quality_score"] == 95.0
    assert pd.isna(cleaned.loc[1, "quality_score"])


def test_clean_preserves_existing_missing_values() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001"],
            "production_date": ["2025-01-01"],
            "production_line": ["Line 1"],
            "shift": ["Morning"],
            "supplier_id": [None],
            "quality_score": [None],
            "units_produced": [100],
            "defective_units": [3],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert pd.isna(cleaned.loc[0, "supplier_id"])
    assert pd.isna(cleaned.loc[0, "quality_score"])


def test_clean_does_not_modify_original_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001"],
            "production_date": ["2025-01-01"],
            "production_line": [" Line 3 "],
            "shift": [" NIGHT "],
            "supplier_id": [" SUP-07 "],
            "quality_score": [105.0],
            "units_produced": [100],
            "defective_units": [3],
        }
    )

    original = dataframe.copy(deep=True)

    cleaner = DataCleaner()

    cleaner.clean(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)


def test_clean_flags_invalid_defect_records() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001", "BATCH-002"],
            "production_date": ["2025-01-01", "2025-01-02"],
            "production_line": ["Line 1", "Line 2"],
            "shift": ["Morning", "Afternoon"],
            "supplier_id": ["SUP-01", "SUP-02"],
            "quality_score": [95.0, 94.0],
            "units_produced": [100, 80],
            "defective_units": [3, 87],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert bool(cleaned.loc[0, "valid_defect_data"]) is True
    assert bool(cleaned.loc[1, "valid_defect_data"]) is False


def test_clean_preserves_invalid_defect_record() -> None:
    dataframe = pd.DataFrame(
        {
            "batch_id": ["BATCH-001"],
            "production_date": ["2025-01-01"],
            "production_line": ["Line 1"],
            "shift": ["Morning"],
            "supplier_id": ["SUP-01"],
            "quality_score": [95.0],
            "units_produced": [80],
            "defective_units": [87],
        }
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean(dataframe)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "units_produced"] == 80
    assert cleaned.loc[0, "defective_units"] == 87
    assert bool(cleaned.loc[0, "valid_defect_data"]) is False
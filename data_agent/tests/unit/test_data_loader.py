from pathlib import Path

import pandas as pd
import pytest

from app.services.data_loader import DataLoader


def test_load_dataset_success(tmp_path: Path) -> None:
    dataset_path = tmp_path / "dataset.csv"
    dataset_path.write_text(
        "batch_id,units_produced\nBATCH-001,100\nBATCH-002,120\n",
        encoding="utf-8",
    )

    loader = DataLoader(dataset_path)

    dataframe = loader.load()

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 2
    assert list(dataframe.columns) == ["batch_id", "units_produced"]


def test_load_dataset_raises_error_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    dataset_path = tmp_path / "missing.csv"

    loader = DataLoader(dataset_path)

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_load_dataset_raises_error_when_path_is_directory(
    tmp_path: Path,
) -> None:
    loader = DataLoader(tmp_path)

    with pytest.raises(ValueError, match="Dataset path is not a file"):
        loader.load()


def test_load_dataset_raises_error_when_dataset_is_empty(
    tmp_path: Path,
) -> None:
    dataset_path = tmp_path / "empty.csv"
    dataset_path.write_text("batch_id,units_produced\n", encoding="utf-8")

    loader = DataLoader(dataset_path)

    with pytest.raises(ValueError, match="Dataset is empty"):
        loader.load()

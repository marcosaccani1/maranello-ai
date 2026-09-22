import pandas as pd
import pytest

from app.services.dataset_repository import DatasetRepository


class CountingLoader:
    def __init__(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        self.dataframe = dataframe
        self.load_calls = 0

    def load(self) -> pd.DataFrame:
        self.load_calls += 1

        return self.dataframe.copy()


class CountingCleaner:
    def __init__(self) -> None:
        self.clean_calls = 0

    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        self.clean_calls += 1

        cleaned = dataframe.copy()
        cleaned["cleaned"] = True

        return cleaned


class FailingLoader:
    def load(self) -> pd.DataFrame:
        raise RuntimeError(
            "Dataset reload failed."
        )


def build_repository() -> tuple[
    DatasetRepository,
    CountingLoader,
    CountingCleaner,
]:
    dataframe = pd.DataFrame(
        {
            "batch_id": [
                "BATCH-001",
                "BATCH-002",
            ],
        }
    )

    loader = CountingLoader(dataframe)
    cleaner = CountingCleaner()

    repository = DatasetRepository(
        loader=loader,
        cleaner=cleaner,
    )

    return repository, loader, cleaner


def test_get_loads_and_cleans_dataset_once() -> None:
    repository, loader, cleaner = (
        build_repository()
    )

    first = repository.get()
    second = repository.get()
    third = repository.get()

    assert loader.load_calls == 1
    assert cleaner.clean_calls == 1

    assert repository.is_loaded is True

    assert first is second
    assert second is third

    assert first["cleaned"].all()


def test_reload_rebuilds_cached_dataset() -> None:
    repository, loader, cleaner = (
        build_repository()
    )

    first = repository.get()
    reloaded = repository.reload()
    cached = repository.get()

    assert loader.load_calls == 2
    assert cleaner.clean_calls == 2

    assert reloaded is cached
    assert reloaded is not first


def test_repository_starts_without_loaded_dataset() -> None:
    repository, loader, cleaner = (
        build_repository()
    )

    assert repository.is_loaded is False
    assert loader.load_calls == 0
    assert cleaner.clean_calls == 0


def test_failed_reload_preserves_existing_cache() -> None:
    repository, _, cleaner = (
        build_repository()
    )

    cached = repository.get()

    repository.loader = FailingLoader()

    with pytest.raises(
        RuntimeError,
        match="Dataset reload failed",
    ):
        repository.reload()

    assert repository.is_loaded is True
    assert repository.get() is cached
    assert cleaner.clean_calls == 1
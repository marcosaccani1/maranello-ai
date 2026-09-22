from threading import Lock

import pandas as pd

from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader


class DatasetRepository:
    """Provide cached access to the prepared manufacturing dataset."""

    def __init__(
        self,
        loader: DataLoader,
        cleaner: DataCleaner,
    ) -> None:
        self.loader = loader
        self.cleaner = cleaner

        self._dataframe: pd.DataFrame | None = None
        self._lock = Lock()

    @property
    def is_loaded(self) -> bool:
        """Return whether the prepared dataset is currently cached."""
        return self._dataframe is not None

    def get(self) -> pd.DataFrame:
        """Return the cached dataset, loading and cleaning it if necessary."""
        if self._dataframe is not None:
            return self._dataframe

        with self._lock:
            if self._dataframe is None:
                self._dataframe = self._load_and_clean()

        return self._dataframe

    def reload(self) -> pd.DataFrame:
        """Reload, clean and replace the cached dataset."""
        dataframe = self._load_and_clean()

        with self._lock:
            self._dataframe = dataframe

        return dataframe

    def _load_and_clean(self) -> pd.DataFrame:
        dataframe = self.loader.load()

        return self.cleaner.clean(
            dataframe
        )
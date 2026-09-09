from pathlib import Path

import pandas as pd


class DataLoader:
    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = dataset_path

    def load(self) -> pd.DataFrame:
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found at: {self.dataset_path}")

        if not self.dataset_path.is_file():
            raise ValueError(f"Dataset path is not a file: {self.dataset_path}")

        dataframe = pd.read_csv(self.dataset_path)

        if dataframe.empty:
            raise ValueError("Dataset is empty.")

        return dataframe

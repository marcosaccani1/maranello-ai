import pandas as pd


class DataCleaner:
    def clean(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        cleaned = dataframe.copy()

        cleaned = self._remove_duplicates(cleaned)
        cleaned = self._normalize_text_fields(cleaned)
        cleaned = self._normalize_dates(cleaned)
        cleaned = self._invalidate_quality_scores(cleaned)
        cleaned = self._flag_invalid_defect_records(cleaned)

        return cleaned

    @staticmethod
    def _remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.drop_duplicates().reset_index(drop=True)

    @staticmethod
    def _normalize_text_fields(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe["production_line"] = dataframe["production_line"].str.strip()

        dataframe["shift"] = (
            dataframe["shift"]
            .str.strip()
            .str.lower()
            .str.capitalize()
        )

        dataframe["supplier_id"] = dataframe["supplier_id"].str.strip()

        return dataframe

    @staticmethod
    def _normalize_dates(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe["production_date"] = pd.to_datetime(
            dataframe["production_date"],
            format="mixed",
            errors="coerce",
        )

        return dataframe

    @staticmethod
    def _invalidate_quality_scores(dataframe: pd.DataFrame) -> pd.DataFrame:
        valid_quality_score = dataframe["quality_score"].between(
            0,
            100,
            inclusive="both",
        )

        dataframe.loc[
            dataframe["quality_score"].notna() & ~valid_quality_score,
            "quality_score",
        ] = pd.NA

        return dataframe

    @staticmethod
    def _flag_invalid_defect_records(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        dataframe["valid_defect_data"] = (
            dataframe["units_produced"].notna()
            & dataframe["defective_units"].notna()
            & (dataframe["units_produced"] > 0)
            & (dataframe["defective_units"] >= 0)
            & (
                dataframe["defective_units"]
                <= dataframe["units_produced"]
            )
        )
    
        return dataframe
from pathlib import Path

import duckdb

from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader


class DuckDBDatasetStore:
    """Persist the prepared manufacturing dataset in DuckDB."""

    TABLE_NAME = "manufacturing_data"

    def __init__(
        self,
        database_path: Path,
        loader: DataLoader,
        cleaner: DataCleaner,
    ) -> None:
        self.database_path = database_path
        self.loader = loader
        self.cleaner = cleaner

    def initialize(self) -> None:
        """Create the persistent dataset only when it is not initialized."""
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.is_initialized():
            return

        self.reload()

    def reload(self) -> None:
        """Reload and atomically replace the prepared DuckDB dataset."""
        dataframe = self.cleaner.clean(
            self.loader.load()
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = duckdb.connect(
            str(self.database_path)
        )

        try:
            connection.register(
                "prepared_dataframe",
                dataframe,
            )

            connection.execute("BEGIN TRANSACTION")

            try:
                connection.execute(
                    """
                    CREATE OR REPLACE TABLE manufacturing_data_staging AS
                    SELECT
                        CAST(batch_id AS VARCHAR) AS batch_id,
                        CAST(production_date AS TIMESTAMP) AS production_date,
                        CAST(plant AS VARCHAR) AS plant,
                        CAST(production_line AS VARCHAR) AS production_line,
                        CAST(vehicle_model AS VARCHAR) AS vehicle_model,
                        CAST(shift AS VARCHAR) AS shift,
                        CAST(units_produced AS BIGINT) AS units_produced,
                        CAST(defective_units AS BIGINT) AS defective_units,
                        CAST(defect_category AS VARCHAR) AS defect_category,
                        CAST(rework_units AS BIGINT) AS rework_units,
                        CAST(scrap_units AS BIGINT) AS scrap_units,
                        CAST(downtime_minutes AS DOUBLE) AS downtime_minutes,
                        CAST(cycle_time_seconds AS DOUBLE) AS cycle_time_seconds,
                        CAST(quality_score AS DOUBLE) AS quality_score,
                        CAST(supplier_id AS VARCHAR) AS supplier_id,
                        CAST(component_category AS VARCHAR) AS component_category,
                        CAST(inspection_status AS VARCHAR) AS inspection_status,
                        CAST(temperature_c AS DOUBLE) AS temperature_c,
                        CAST(operator_team AS VARCHAR) AS operator_team,
                        CAST(notes AS VARCHAR) AS notes,
                        CAST(valid_defect_data AS BOOLEAN) AS valid_defect_data
                    FROM prepared_dataframe
                    """
                )

                connection.execute(
                    f"DROP TABLE IF EXISTS {self.TABLE_NAME}"
                )

                connection.execute(
                    f"""
                    ALTER TABLE manufacturing_data_staging
                    RENAME TO {self.TABLE_NAME}
                    """
                )

                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        finally:
            connection.unregister(
                "prepared_dataframe"
            )
            connection.close()

    def is_initialized(self) -> bool:
        """Return whether the persistent dataset is ready for queries."""
        if not self.database_path.exists():
            return False

        connection = duckdb.connect(
            str(self.database_path),
            read_only=True,
        )

        try:
            result = connection.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'main'
                  AND table_name = ?
                """,
                [self.TABLE_NAME],
            ).fetchone()

            if result is None or int(result[0]) != 1:
                return False

            row_count = connection.execute(
                f"SELECT COUNT(*) FROM {self.TABLE_NAME}"
            ).fetchone()

            return (
                row_count is not None
                and int(row_count[0]) > 0
            )
        finally:
            connection.close()
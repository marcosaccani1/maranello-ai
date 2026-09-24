from pathlib import Path

import duckdb

from app.models.analysis import (
    GroupedMetric,
    ManufacturingKPIs,
    MonthlyTrendMetric,
)


class DuckDBAnalysisRepository:
    """Execute manufacturing analytics directly in DuckDB."""

    ALLOWED_GROUP_DIMENSIONS = {
        "production_line",
        "shift",
        "supplier_id",
        "component_category",
        "vehicle_model",
        "plant",
        "operator_team",
    }

    def __init__(
        self,
        database_path: Path,
    ) -> None:
        self.database_path = database_path

    def calculate_kpis(
        self,
    ) -> ManufacturingKPIs:
        row = self._fetchone(
            """
            SELECT
                COALESCE(
                    SUM(units_produced)
                        FILTER (WHERE valid_defect_data),
                    0
                ) AS total_production,
                COALESCE(
                    SUM(defective_units)
                        FILTER (WHERE valid_defect_data),
                    0
                ) AS total_defective_units,
                COALESCE(
                    SUM(rework_units)
                        FILTER (WHERE valid_defect_data),
                    0
                ) AS total_rework_units,
                COALESCE(
                    SUM(scrap_units)
                        FILTER (WHERE valid_defect_data),
                    0
                ) AS total_scrap_units,
                AVG(quality_score) AS average_quality_score,
                AVG(downtime_minutes) AS average_downtime_minutes,
                AVG(cycle_time_seconds) AS average_cycle_time_seconds
            FROM manufacturing_data
            """
        )

        total_production = int(row[0])
        total_defective_units = int(row[1])
        total_rework_units = int(row[2])
        total_scrap_units = int(row[3])

        return ManufacturingKPIs(
            total_production=total_production,
            total_defective_units=total_defective_units,
            defect_rate=self._calculate_rate(
                total_defective_units,
                total_production,
            ),
            rework_rate=self._calculate_rate(
                total_rework_units,
                total_production,
            ),
            scrap_rate=self._calculate_rate(
                total_scrap_units,
                total_production,
            ),
            average_quality_score=self._round_nullable(
                row[4]
            ),
            average_downtime_minutes=self._round_nullable(
                row[5]
            ),
            average_cycle_time_seconds=self._round_nullable(
                row[6]
            ),
        )

    def calculate_defect_rate_by(
        self,
        dimension: str,
    ) -> list[GroupedMetric]:
        if dimension not in self.ALLOWED_GROUP_DIMENSIONS:
            raise ValueError(
                f"Unsupported grouping dimension: {dimension}"
            )

        rows = self._fetchall(
            f"""
            SELECT
                {dimension} AS group_value,
                SUM(units_produced) AS total_production,
                SUM(defective_units) AS total_defective_units
            FROM manufacturing_data
            WHERE valid_defect_data = TRUE
              AND {dimension} IS NOT NULL
            GROUP BY {dimension}
            """
        )

        results = [
            GroupedMetric(
                group=str(row[0]),
                total_production=int(row[1]),
                total_defective_units=int(row[2]),
                defect_rate=self._calculate_rate(
                    row[2],
                    row[1],
                ),
            )
            for row in rows
        ]

        return sorted(
            results,
            key=lambda item: item.defect_rate,
            reverse=True,
        )

    def calculate_monthly_trend(
        self,
    ) -> list[MonthlyTrendMetric]:
        rows = self._fetchall(
            """
            SELECT
                STRFTIME(production_date, '%Y-%m') AS period,
                COALESCE(
                    SUM(units_produced)
                        FILTER (WHERE valid_defect_data),
                    0
                ) AS total_production,
                COALESCE(
                    SUM(defective_units)
                        FILTER (WHERE valid_defect_data),
                    0
                ) AS total_defective_units,
                AVG(quality_score) AS average_quality_score,
                AVG(downtime_minutes) AS average_downtime_minutes
            FROM manufacturing_data
            WHERE production_date IS NOT NULL
            GROUP BY period
            ORDER BY period
            """
        )

        return [
            MonthlyTrendMetric(
                period=str(row[0]),
                total_production=int(row[1]),
                total_defective_units=int(row[2]),
                defect_rate=self._calculate_rate(
                    row[2],
                    row[1],
                ),
                average_quality_score=self._round_nullable(
                    row[3]
                ),
                average_downtime_minutes=self._round_nullable(
                    row[4]
                ),
            )
            for row in rows
        ]

    def _fetchone(
        self,
        query: str,
    ) -> tuple:
        connection = self._connect()

        try:
            row = connection.execute(query).fetchone()

            if row is None:
                raise RuntimeError(
                    "DuckDB query returned no result."
                )

            return row
        finally:
            connection.close()

    def _fetchall(
        self,
        query: str,
    ) -> list[tuple]:
        connection = self._connect()

        try:
            return connection.execute(query).fetchall()
        finally:
            connection.close()

    def _connect(
        self,
    ) -> duckdb.DuckDBPyConnection:
        if not self.database_path.exists():
            raise FileNotFoundError(
                f"DuckDB database not found at: {self.database_path}"
            )

        return duckdb.connect(
            str(self.database_path),
            read_only=True,
        )

    @staticmethod
    def _calculate_rate(
        numerator: int | float,
        denominator: int | float,
    ) -> float:
        if denominator <= 0:
            return 0.0

        return round(
            (numerator / denominator) * 100,
            2,
        )

    @staticmethod
    def _round_nullable(
        value: float | None,
    ) -> float | None:
        if value is None:
            return None

        return round(
            float(value),
            2,
        )
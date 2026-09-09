import pandas as pd

from app.models.analysis import (
    GroupedMetric,
    ManufacturingKPIs,
    MonthlyTrendMetric,
)


class AnalysisService:
    ALLOWED_GROUP_DIMENSIONS = {
        "production_line",
        "shift",
        "supplier_id",
        "component_category",
        "vehicle_model",
        "plant",
        "operator_team",
    }

    def calculate_kpis(
        self,
        dataframe: pd.DataFrame,
    ) -> ManufacturingKPIs:
        valid_defect_data = dataframe[dataframe["valid_defect_data"]]

        total_production = int(valid_defect_data["units_produced"].sum())
        total_defective_units = int(
            valid_defect_data["defective_units"].sum()
        )

        defect_rate = self._calculate_rate(
            numerator=total_defective_units,
            denominator=total_production,
        )

        total_rework_units = int(
            valid_defect_data["rework_units"].sum()
        )
        rework_rate = self._calculate_rate(
            numerator=total_rework_units,
            denominator=total_production,
        )

        total_scrap_units = int(
            valid_defect_data["scrap_units"].sum()
        )
        scrap_rate = self._calculate_rate(
            numerator=total_scrap_units,
            denominator=total_production,
        )

        return ManufacturingKPIs(
            total_production=total_production,
            total_defective_units=total_defective_units,
            defect_rate=defect_rate,
            rework_rate=rework_rate,
            scrap_rate=scrap_rate,
            average_quality_score=self._safe_mean(
                dataframe["quality_score"]
            ),
            average_downtime_minutes=self._safe_mean(
                dataframe["downtime_minutes"]
            ),
            average_cycle_time_seconds=self._safe_mean(
                dataframe["cycle_time_seconds"]
            ),
        )

    def calculate_defect_rate_by(
        self,
        dataframe: pd.DataFrame,
        dimension: str,
    ) -> list[GroupedMetric]:
        if dimension not in self.ALLOWED_GROUP_DIMENSIONS:
            raise ValueError(
                f"Unsupported grouping dimension: {dimension}"
            )

        valid_data = dataframe[
            dataframe["valid_defect_data"]
        ].copy()

        valid_data = valid_data[
            valid_data[dimension].notna()
        ]

        grouped = (
            valid_data.groupby(
                dimension,
                dropna=False,
            )
            .agg(
                total_production=(
                    "units_produced",
                    "sum",
                ),
                total_defective_units=(
                    "defective_units",
                    "sum",
                ),
            )
            .reset_index()
        )

        results = [
            GroupedMetric(
                group=str(row[dimension]),
                total_production=int(
                    row["total_production"]
                ),
                total_defective_units=int(
                    row["total_defective_units"]
                ),
                defect_rate=self._calculate_rate(
                    numerator=row[
                        "total_defective_units"
                    ],
                    denominator=row[
                        "total_production"
                    ],
                ),
            )
            for _, row in grouped.iterrows()
        ]

        return sorted(
            results,
            key=lambda item: item.defect_rate,
            reverse=True,
        )

    def calculate_monthly_trend(
        self,
        dataframe: pd.DataFrame,
    ) -> list[MonthlyTrendMetric]:
        valid_dates = dataframe[
            dataframe["production_date"].notna()
        ].copy()

        if valid_dates.empty:
            return []

        valid_dates["period"] = (
            valid_dates["production_date"]
            .dt.to_period("M")
            .astype(str)
        )

        results: list[MonthlyTrendMetric] = []

        for period, group in valid_dates.groupby(
            "period",
            sort=True,
        ):
            valid_defect_data = group[
                group["valid_defect_data"]
            ]

            total_production = int(
                valid_defect_data[
                    "units_produced"
                ].sum()
            )

            total_defective_units = int(
                valid_defect_data[
                    "defective_units"
                ].sum()
            )

            results.append(
                MonthlyTrendMetric(
                    period=str(period),
                    total_production=total_production,
                    total_defective_units=(
                        total_defective_units
                    ),
                    defect_rate=self._calculate_rate(
                        numerator=(
                            total_defective_units
                        ),
                        denominator=total_production,
                    ),
                    average_quality_score=(
                        self._safe_mean(
                            group["quality_score"]
                        )
                    ),
                    average_downtime_minutes=(
                        self._safe_mean(
                            group[
                                "downtime_minutes"
                            ]
                        )
                    ),
                )
            )

        return results

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
    def _safe_mean(
        series: pd.Series,
    ) -> float | None:
        mean = series.mean()

        if pd.isna(mean):
            return None

        return round(
            float(mean),
            2,
        )
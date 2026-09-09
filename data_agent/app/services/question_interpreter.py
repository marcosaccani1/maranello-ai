from dataclasses import dataclass
from typing import Literal

AnalysisType = Literal[
    "global_kpis",
    "grouped_defect_rate",
    "monthly_trend",
]


@dataclass(frozen=True)
class AnalysisPlan:
    analysis_type: AnalysisType
    dimension: str | None = None


class QuestionInterpreter:
    DIMENSION_KEYWORDS = {
        "production_line": {
            "production line",
            "production lines",
            "line",
            "lines",
            "linea",
            "linee",
            "linea produttiva",
            "linee produttive",
        },
        "shift": {
            "shift",
            "shifts",
            "turno",
            "turni",
        },
        "supplier_id": {
            "supplier",
            "suppliers",
            "vendor",
            "vendors",
            "fornitore",
            "fornitori",
        },
        "component_category": {
            "component",
            "components",
            "component category",
            "component categories",
            "componente",
            "componenti",
            "categoria componente",
            "categorie componenti",
        },
        "vehicle_model": {
            "vehicle model",
            "vehicle models",
            "model",
            "models",
            "modello",
            "modelli",
            "modello veicolo",
            "modelli veicolo",
        },
        "plant": {
            "plant",
            "plants",
            "factory",
            "factories",
            "stabilimento",
            "stabilimenti",
        },
        "operator_team": {
            "operator team",
            "operator teams",
            "team",
            "teams",
            "squadra",
            "squadre",
            "team operatori",
        },
    }

    TEMPORAL_KEYWORDS = {
        "monthly",
        "month",
        "months",
        "month over month",
        "over time",
        "trend",
        "mensile",
        "mese",
        "mesi",
        "mese per mese",
        "nel tempo",
        "andamento",
        "trend mensile",
    }

    def interpret(
        self,
        question: str,
    ) -> AnalysisPlan:
        normalized_question = self._normalize(question)

        if not normalized_question:
            raise ValueError(
                "Analysis question cannot be empty."
            )

        dimension = self._detect_dimension(
            normalized_question
        )

        has_temporal_intent = self._contains_any(
            normalized_question,
            self.TEMPORAL_KEYWORDS,
        )

        if has_temporal_intent and dimension is not None:
            raise ValueError(
                "Combined temporal and grouped analysis "
                "is not supported yet."
            )

        if has_temporal_intent:
            return AnalysisPlan(
                analysis_type="monthly_trend",
            )

        if dimension is not None:
            return AnalysisPlan(
                analysis_type="grouped_defect_rate",
                dimension=dimension,
            )

        return AnalysisPlan(
            analysis_type="global_kpis",
        )

    def _detect_dimension(
        self,
        question: str,
    ) -> str | None:
        detected_dimensions = [
            dimension
            for dimension, keywords
            in self.DIMENSION_KEYWORDS.items()
            if self._contains_any(
                question,
                keywords,
            )
        ]

        if len(detected_dimensions) > 1:
            raise ValueError(
                "Multiple grouping dimensions were detected. "
                "Only one grouping dimension is supported "
                "per analysis."
            )

        if not detected_dimensions:
            return None

        return detected_dimensions[0]

    @staticmethod
    def _contains_any(
        question: str,
        keywords: set[str],
    ) -> bool:
        return any(
            keyword in question
            for keyword in keywords
        )

    @staticmethod
    def _normalize(
        question: str,
    ) -> str:
        return " ".join(
            question.casefold().split()
        )
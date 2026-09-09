import pytest

from app.services.question_interpreter import (
    QuestionInterpreter,
)


def test_interpret_global_kpis_in_english() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "What is the overall manufacturing performance?"
    )

    assert plan.analysis_type == "global_kpis"
    assert plan.dimension is None


def test_interpret_global_kpis_in_italian() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Qual è la performance generale della produzione?"
    )

    assert plan.analysis_type == "global_kpis"
    assert plan.dimension is None


def test_interpret_supplier_analysis_in_english() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Which supplier has the highest defect rate?"
    )

    assert plan.analysis_type == "grouped_defect_rate"
    assert plan.dimension == "supplier_id"


def test_interpret_supplier_analysis_in_italian() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Quale fornitore ha il defect rate più alto?"
    )

    assert plan.analysis_type == "grouped_defect_rate"
    assert plan.dimension == "supplier_id"


def test_interpret_production_line_analysis() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Compare the defect rate across production lines."
    )

    assert plan.analysis_type == "grouped_defect_rate"
    assert plan.dimension == "production_line"


def test_interpret_shift_analysis_in_italian() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Quale turno presenta più difetti?"
    )

    assert plan.analysis_type == "grouped_defect_rate"
    assert plan.dimension == "shift"


def test_interpret_monthly_trend_in_english() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Show me the monthly defect rate trend."
    )

    assert plan.analysis_type == "monthly_trend"
    assert plan.dimension is None


def test_interpret_monthly_trend_in_italian() -> None:
    interpreter = QuestionInterpreter()

    plan = interpreter.interpret(
        "Mostrami l'andamento mensile del defect rate."
    )

    assert plan.analysis_type == "monthly_trend"
    assert plan.dimension is None


def test_interpret_rejects_multiple_dimensions() -> None:
    interpreter = QuestionInterpreter()

    with pytest.raises(
        ValueError,
        match="Multiple grouping dimensions",
    ):
        interpreter.interpret(
            "Compare suppliers across production lines."
        )


def test_interpret_rejects_grouped_monthly_request() -> None:
    interpreter = QuestionInterpreter()

    with pytest.raises(
        ValueError,
        match="Combined temporal and grouped analysis",
    ):
        interpreter.interpret(
            "Show the monthly defect trend by supplier."
        )


def test_interpret_rejects_empty_question() -> None:
    interpreter = QuestionInterpreter()

    with pytest.raises(
        ValueError,
        match="Analysis question cannot be empty",
    ):
        interpreter.interpret("   ")
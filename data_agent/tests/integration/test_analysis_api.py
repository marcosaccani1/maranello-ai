from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analysis_endpoint_returns_global_kpis() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": (
                "What is the overall manufacturing performance?"
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["success"] is True
    assert payload["error"] is None

    result = payload["result"]

    assert result is not None
    assert result["analysis_type"] == "global_kpis"
    assert result["chart_url"] is None

    data = result["data"]

    assert data["total_production"] > 0
    assert data["total_defective_units"] > 0
    assert data["defect_rate"] > 0

    assert "total_production" in data
    assert "rework_rate" in data
    assert "scrap_rate" in data
    assert "average_quality_score" in data
    assert "average_downtime_minutes" in data
    assert "average_cycle_time_seconds" in data

    assert result["summary"]


def test_analysis_endpoint_rejects_empty_question() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": "",
        },
    )

    assert response.status_code == 422


def test_analysis_endpoint_rejects_missing_question() -> None:
    response = client.post(
        "/api/analysis",
        json={},
    )

    assert response.status_code == 422


def test_analysis_endpoint_rejects_question_over_maximum_length() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": "a" * 1001,
        },
    )

    assert response.status_code == 422
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analysis_endpoint_routes_global_question() -> None:
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
    assert (
        payload["result"]["analysis_type"]
        == "global_kpis"
    )


def test_analysis_endpoint_routes_supplier_question() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": (
                "Which supplier has the highest defect rate?"
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()
    result = payload["result"]

    assert result["analysis_type"] == (
        "grouped_defect_rate"
    )

    assert result["data"][0]["group"] == "SUP-07"

    assert result["data"][0]["defect_rate"] > 0


def test_analysis_endpoint_routes_italian_supplier_question() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": (
                "Quale fornitore ha il defect rate più alto?"
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()
    result = payload["result"]

    assert result["analysis_type"] == (
        "grouped_defect_rate"
    )

    assert result["data"][0]["group"] == "SUP-07"


def test_analysis_endpoint_routes_monthly_trend_question() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": (
                "Show me the monthly defect rate trend."
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()
    result = payload["result"]

    assert result["analysis_type"] == "monthly_trend"

    assert result["chart_url"] is not None

    assert result["chart_url"].startswith(
        "/charts/monthly_defect_rate_"
    )

    assert len(result["data"]) == 12


def test_analysis_endpoint_rejects_unsupported_combined_analysis() -> None:
    response = client.post(
        "/api/analysis",
        json={
            "question": (
                "Show the monthly defect trend by supplier."
            )
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert (
        "Combined temporal and grouped analysis"
        in payload["detail"]
    )
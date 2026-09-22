import asyncio
from unittest.mock import Mock

from fastapi.testclient import TestClient

import app.main as main_module


def test_lifespan_runs_initial_chart_cleanup(
    monkeypatch,
) -> None:
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    with TestClient(main_module.app):
        pass

    cleanup_mock.assert_called_once()


def test_lifespan_keeps_application_available(
    monkeypatch,
) -> None:
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    with TestClient(main_module.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cleanup_loop_runs_periodic_cleanup(
    monkeypatch,
) -> None:
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    sleep_calls = 0

    async def fake_sleep(
        delay: float,
    ) -> None:
        nonlocal sleep_calls

        assert delay == (
            main_module.settings
            .chart_cleanup_interval_minutes
            * 60
        )

        sleep_calls += 1

        if sleep_calls > 1:
            raise asyncio.CancelledError

    monkeypatch.setattr(
        main_module.asyncio,
        "sleep",
        fake_sleep,
    )

    async def run_test() -> None:
        try:
            await main_module.run_chart_cleanup_loop()
        except asyncio.CancelledError:
            pass

    asyncio.run(run_test())

    cleanup_mock.assert_called_once()


def test_lifespan_cancels_periodic_task_on_shutdown(
    monkeypatch,
) -> None:
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    task_started = asyncio.Event()
    task_cancelled = asyncio.Event()

    async def fake_cleanup_loop() -> None:
        task_started.set()

        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            task_cancelled.set()
            raise

    monkeypatch.setattr(
        main_module,
        "run_chart_cleanup_loop",
        fake_cleanup_loop,
    )

    async def run_test() -> None:
        async with main_module.lifespan(
            main_module.app
        ):
            await task_started.wait()

        assert task_cancelled.is_set()

    asyncio.run(run_test())
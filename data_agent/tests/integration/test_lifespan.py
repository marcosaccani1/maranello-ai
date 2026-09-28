import asyncio
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import app.main as main_module


def test_validate_analytical_database_accepts_prepared_database(
    monkeypatch,
) -> None:
    store_mock = Mock()
    store_mock.is_initialized.return_value = True

    store_factory_mock = Mock(
        return_value=store_mock
    )

    monkeypatch.setattr(
        main_module,
        "DuckDBDatasetStore",
        store_factory_mock,
    )

    main_module.validate_analytical_database()

    store_factory_mock.assert_called_once_with(
        database_path=main_module.settings.database_path,
    )

    store_mock.is_initialized.assert_called_once_with()


def test_validate_analytical_database_rejects_unprepared_database(
    monkeypatch,
) -> None:
    store_mock = Mock()
    store_mock.is_initialized.return_value = False

    store_factory_mock = Mock(
        return_value=store_mock
    )

    monkeypatch.setattr(
        main_module,
        "DuckDBDatasetStore",
        store_factory_mock,
    )

    with pytest.raises(
        RuntimeError,
        match="Analytical database is not initialized",
    ):
        main_module.validate_analytical_database()

    store_factory_mock.assert_called_once_with(
        database_path=main_module.settings.database_path,
    )

    store_mock.is_initialized.assert_called_once_with()


def test_lifespan_runs_database_validation_before_chart_cleanup(
    monkeypatch,
) -> None:
    call_order: list[str] = []

    def validate_database() -> None:
        call_order.append(
            "database_validation"
        )

    def cleanup_charts() -> int:
        call_order.append(
            "chart_cleanup"
        )
        return 0

    monkeypatch.setattr(
        main_module,
        "validate_analytical_database",
        validate_database,
    )

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_charts,
    )

    with TestClient(main_module.app):
        pass

    assert call_order[:2] == [
        "database_validation",
        "chart_cleanup",
    ]


def test_lifespan_fails_before_runtime_when_database_is_not_ready(
    monkeypatch,
) -> None:
    cleanup_mock = Mock(return_value=0)

    def reject_database() -> None:
        raise RuntimeError(
            "Analytical database is not initialized."
        )

    monkeypatch.setattr(
        main_module,
        "validate_analytical_database",
        reject_database,
    )

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    with pytest.raises(
        RuntimeError,
        match="Analytical database is not initialized",
    ):
        with TestClient(main_module.app):
            pass

    cleanup_mock.assert_not_called()


def test_lifespan_runs_initial_chart_cleanup(
    monkeypatch,
) -> None:
    validation_mock = Mock()
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module,
        "validate_analytical_database",
        validation_mock,
    )

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    with TestClient(main_module.app):
        pass

    validation_mock.assert_called_once()
    cleanup_mock.assert_called_once()


def test_lifespan_keeps_application_available(
    monkeypatch,
) -> None:
    validation_mock = Mock()
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module,
        "validate_analytical_database",
        validation_mock,
    )

    monkeypatch.setattr(
        main_module.chart_cleanup_service,
        "cleanup",
        cleanup_mock,
    )

    with TestClient(main_module.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    validation_mock.assert_called_once()


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
    validation_mock = Mock()
    cleanup_mock = Mock(return_value=0)

    monkeypatch.setattr(
        main_module,
        "validate_analytical_database",
        validation_mock,
    )

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

    validation_mock.assert_called_once()
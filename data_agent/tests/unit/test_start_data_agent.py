from unittest.mock import Mock, call

import pytest

import app.commands.start_data_agent as start_module


def test_resolve_worker_count_uses_configured_value(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        start_module.settings,
        "data_agent_workers",
        3,
    )

    assert start_module.resolve_worker_count() == 3


def test_start_data_agent_prepares_once_before_single_worker_start(
    monkeypatch,
) -> None:
    lifecycle_mock = Mock()

    def prepare_database() -> None:
        lifecycle_mock("prepare_database")

    def run_uvicorn(
        app: str,
        **kwargs,
    ) -> None:
        lifecycle_mock(
            "uvicorn_run",
            app,
            kwargs,
        )

    monkeypatch.setattr(
        start_module.settings,
        "data_agent_workers",
        1,
    )

    monkeypatch.setattr(
        start_module,
        "prepare_database",
        prepare_database,
    )

    monkeypatch.setattr(
        start_module.uvicorn,
        "run",
        run_uvicorn,
    )

    start_module.start_data_agent()

    assert lifecycle_mock.call_args_list == [
        call("prepare_database"),
        call(
            "uvicorn_run",
            "app.main:app",
            {
                "host": start_module.DEFAULT_HOST,
                "port": start_module.DEFAULT_PORT,
                "workers": 1,
            },
        ),
    ]


def test_start_data_agent_prepares_once_before_multi_worker_start(
    monkeypatch,
) -> None:
    lifecycle_mock = Mock()

    def prepare_database() -> None:
        lifecycle_mock("prepare_database")

    def run_uvicorn(
        app: str,
        **kwargs,
    ) -> None:
        lifecycle_mock(
            "uvicorn_run",
            app,
            kwargs,
        )

    monkeypatch.setattr(
        start_module.settings,
        "data_agent_workers",
        3,
    )

    monkeypatch.setattr(
        start_module,
        "prepare_database",
        prepare_database,
    )

    monkeypatch.setattr(
        start_module.uvicorn,
        "run",
        run_uvicorn,
    )

    start_module.start_data_agent()

    assert lifecycle_mock.call_args_list == [
        call("prepare_database"),
        call(
            "uvicorn_run",
            "app.main:app",
            {
                "host": start_module.DEFAULT_HOST,
                "port": start_module.DEFAULT_PORT,
                "workers": 3,
            },
        ),
    ]


def test_start_data_agent_does_not_start_workers_when_preparation_fails(
    monkeypatch,
) -> None:
    uvicorn_run_mock = Mock()

    def fail_preparation() -> None:
        raise RuntimeError("Database preparation failed.")

    monkeypatch.setattr(
        start_module.settings,
        "data_agent_workers",
        3,
    )

    monkeypatch.setattr(
        start_module,
        "prepare_database",
        fail_preparation,
    )

    monkeypatch.setattr(
        start_module.uvicorn,
        "run",
        uvicorn_run_mock,
    )

    with pytest.raises(
        RuntimeError,
        match="Database preparation failed",
    ):
        start_module.start_data_agent()

    uvicorn_run_mock.assert_not_called()

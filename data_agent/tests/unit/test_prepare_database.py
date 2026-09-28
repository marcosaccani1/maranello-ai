from unittest.mock import Mock

import pytest

import app.commands.prepare_database as prepare_module


def test_prepare_database_rebuilds_and_validates_dataset(
    monkeypatch,
) -> None:
    store_mock = Mock()
    store_mock.is_initialized.return_value = True

    build_store_mock = Mock(
        return_value=store_mock
    )

    monkeypatch.setattr(
        prepare_module,
        "build_dataset_store",
        build_store_mock,
    )

    prepare_module.prepare_database()

    build_store_mock.assert_called_once_with()
    store_mock.reload.assert_called_once_with()
    store_mock.is_initialized.assert_called_once_with()


def test_prepare_database_fails_when_dataset_is_not_ready(
    monkeypatch,
) -> None:
    store_mock = Mock()
    store_mock.is_initialized.return_value = False

    monkeypatch.setattr(
        prepare_module,
        "build_dataset_store",
        Mock(return_value=store_mock),
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "DuckDB dataset preparation completed "
            "without producing a valid analytical database"
        ),
    ):
        prepare_module.prepare_database()

    store_mock.reload.assert_called_once_with()
    store_mock.is_initialized.assert_called_once_with()


def test_build_dataset_store_uses_configured_paths() -> None:
    store = prepare_module.build_dataset_store()

    assert (
        store.database_path
        == prepare_module.settings.database_path
    )

    assert store.loader is not None

    assert (
        store.loader.dataset_path
        == prepare_module.settings.dataset_path
    )

    assert store.cleaner is not None

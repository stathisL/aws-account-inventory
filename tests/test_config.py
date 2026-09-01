import pytest

from src.config import (
    DEFAULT_PROFILE_NAME,
    DEFAULT_REGION_NAME,
    DEFAULT_ROLE_NAME,
    DEFAULT_LOG_LEVEL,
    get_profile_name,
    get_region_name,
    get_role_name,
    get_log_level
)


def test_get_profile_name_returns_default_when_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AWS_INVENTORY_PROFILE", raising=False)

    assert get_profile_name() == DEFAULT_PROFILE_NAME


def test_get_profile_name_returns_environment_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AWS_INVENTORY_PROFILE", "custom-profile")

    assert get_profile_name() == "custom-profile"


def test_get_role_name_returns_default_when_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AWS_INVENTORY_ROLE", raising=False)

    assert get_role_name() == DEFAULT_ROLE_NAME


def test_get_role_name_returns_environment_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AWS_INVENTORY_ROLE", "CustomInventoryRole")

    assert get_role_name() == "CustomInventoryRole"


def test_get_region_name_returns_default_when_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AWS_INVENTORY_REGION", raising=False)

    assert get_region_name() == DEFAULT_REGION_NAME


def test_get_region_name_returns_environment_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AWS_INVENTORY_REGION", "eu-central-1")

    assert get_region_name() == "eu-central-1"


def test_get_log_level_returns_default_when_not_configured(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("AWS_INVENTORY_LOG_LEVEL", raising=False)

    assert get_log_level() == DEFAULT_LOG_LEVEL


def test_get_log_level_returns_environment_value(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AWS_INVENTORY_LOG_LEVEL", "DEBUG")

    assert get_log_level() == "DEBUG"

from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_stop import (
    SystemdUnitStopItem,
)
from cyberfusion.QueueSupport.outcomes import SystemdUnitStopItemStopOutcome
from cyberfusion.SystemdSupport.units import Unit

# Equal


def test_systemd_unit_stop_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitStopItem(name="example") == SystemdUnitStopItem(name="example")


def test_systemd_unit_stop_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitStopItem(name="example") != SystemdUnitStopItem(name="johndoe")


def test_systemd_unit_stop_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdUnitStopItem(name="example") == 5) is False


# Outcomes


def test_systemd_unit_stop_item_active_has_outcome_stop(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitStopItem(name="example")

    assert SystemdUnitStopItemStopOutcome(unit=Unit("example")) in object_.outcomes


def test_systemd_unit_stop_item_not_active_not_has_outcome_stop(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitStopItem(name="example")

    assert SystemdUnitStopItemStopOutcome(unit=Unit("example")) not in object_.outcomes

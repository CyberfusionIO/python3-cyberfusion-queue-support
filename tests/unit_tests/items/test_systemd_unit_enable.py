from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_enable import (
    SystemdUnitEnableItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdUnitEnableItemEnableOutcome,
)
from cyberfusion.SystemdSupport.units import Unit

# Equal


def test_systemd_unit_enable_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitEnableItem(name="example") == SystemdUnitEnableItem(
        name="example"
    )


def test_systemd_unit_enable_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitEnableItem(name="example") != SystemdUnitEnableItem(
        name="johndoe"
    )


def test_systemd_unit_enable_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdUnitEnableItem(name="example") == 5) is False


# Outcomes


def test_systemd_unit_enable_item_not_enabled_has_outcome_enable(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitEnableItem(name="example")

    assert SystemdUnitEnableItemEnableOutcome(unit=Unit("example")) in object_.outcomes


def test_systemd_unit_enable_item_enabled_not_has_outcome_enable(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitEnableItem(name="example")

    assert not object_.outcomes

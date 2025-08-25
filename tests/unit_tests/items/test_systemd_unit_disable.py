from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_disable import (
    SystemdUnitDisableItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdUnitDisableItemDisableOutcome,
)
from cyberfusion.SystemdSupport.units import Unit
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_systemd_unit_disable_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitDisableItem(name="example") == SystemdUnitDisableItem(
        name="example"
    )


def test_systemd_unit_disable_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitDisableItem(name="example") != SystemdUnitDisableItem(
        name="johndoe"
    )


def test_systemd_unit_disable_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdUnitDisableItem(name="example") == 5) is False


# Outcomes


def test_systemd_unit_disable_item_enabled_has_outcome_disable(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitDisableItem(name="example")

    assert (
        SystemdUnitDisableItemDisableOutcome(unit=Unit("example")) in object_.outcomes
    )


def test_systemd_unit_disable_item_not_enabled_not_has_outcome_disable(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitDisableItem(name="example")

    assert not object_.outcomes


# Serialization


def test_systemd_unit_disable_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdUnitDisableItem(name="example")

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "name": "example",
            "unit": {"name": "example"},
        }
    )

    assert serialized == expected

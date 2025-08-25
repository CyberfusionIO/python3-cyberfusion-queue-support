from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_start import (
    SystemdUnitStartItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdUnitStartItemStartOutcome,
)
from cyberfusion.SystemdSupport.units import Unit
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_systemd_unit_start_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitStartItem(name="example") == SystemdUnitStartItem(name="example")


def test_systemd_unit_start_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitStartItem(name="example") != SystemdUnitStartItem(name="johndoe")


def test_systemd_unit_start_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdUnitStartItem(name="example") == 5) is False


# Outcomes


def test_systemd_unit_start_item_not_started_has_outcome_start(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitStartItem(name="example")

    assert SystemdUnitStartItemStartOutcome(unit=Unit("example")) in object_.outcomes


def test_systemd_unit_start_item_started_not_has_outcome_start(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitStartItem(name="example")

    assert not object_.outcomes


# Serialization


def test_systemd_unit_start_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdUnitStartItem(name="example")

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "name": "example",
            "unit": {"name": "example"},
        }
    )

    assert serialized == expected

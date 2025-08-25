from typing import Generator

from cyberfusion.QueueSupport.items.systemd_unit_restart import (
    SystemdUnitRestartItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdUnitRestartItemRestartOutcome,
)
from cyberfusion.SystemdSupport.units import Unit
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_systemd_unit_restart_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitRestartItem(name="example") == SystemdUnitRestartItem(
        name="example"
    )


def test_systemd_unit_restart_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitRestartItem(name="example") != SystemdUnitRestartItem(
        name="johndoe"
    )


def test_systemd_unit_restart_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdUnitRestartItem(name="example") == 5) is False


# Outcomes


def test_systemd_unit_restart_item_has_outcome_restart(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdUnitRestartItem(name="example")

    assert (
        SystemdUnitRestartItemRestartOutcome(unit=Unit("example")) in object_.outcomes
    )


# Serialization


def test_systemd_unit_restart_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdUnitRestartItem(name="example")

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "name": "example",
            "unit": {"name": "example"},
        }
    )

    assert serialized == expected

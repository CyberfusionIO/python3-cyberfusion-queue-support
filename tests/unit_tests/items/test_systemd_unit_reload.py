from typing import Generator

from cyberfusion.QueueSupport.items.systemd_unit_reload import (
    SystemdUnitReloadItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdUnitReloadItemReloadOutcome,
)
from cyberfusion.SystemdSupport.units import Unit
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_systemd_unit_reload_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitReloadItem(name="example") == SystemdUnitReloadItem(
        name="example"
    )


def test_systemd_unit_reload_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdUnitReloadItem(name="example") != SystemdUnitReloadItem(
        name="johndoe"
    )


def test_systemd_unit_reload_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdUnitReloadItem(name="example") == 5) is False


# Outcomes


def test_systemd_unit_reload_item_has_outcome_reload(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdUnitReloadItem(name="example")

    assert SystemdUnitReloadItemReloadOutcome(unit=Unit("example")) in object_.outcomes


# Serialization


def test_systemd_unit_reload_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdUnitReloadItem(name="example")

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "name": "example",
            "unit": {"name": "example"},
        }
    )

    assert serialized == expected

from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_reload import (
    SystemdUnitReloadItem,
)


def test_systemd_unit_reload_item_fulfill_reload(
    mocker: MockerFixture,
) -> None:
    spy_reload = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.reload", return_value=None
    )

    object_ = SystemdUnitReloadItem(name="example")
    object_.fulfill()

    spy_reload.assert_called_once_with()

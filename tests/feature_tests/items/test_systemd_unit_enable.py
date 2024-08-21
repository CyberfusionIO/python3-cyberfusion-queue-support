from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_enable import (
    SystemdUnitEnableItem,
)


def test_systemd_unit_enable_item_fulfill_enable(
    mocker: MockerFixture,
) -> None:
    spy_enable = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.enable", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitEnableItem(name="example")
    object_.fulfill()

    spy_enable.assert_called_once_with()


def test_systemd_unit_enable_item_fulfill_not_enable(
    mocker: MockerFixture,
) -> None:
    spy_enable = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.enable", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitEnableItem(name="example")
    object_.fulfill()

    spy_enable.assert_not_called()

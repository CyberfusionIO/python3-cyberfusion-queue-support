from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_disable import (
    SystemdUnitDisableItem,
)


def test_systemd_unit_disable_item_fulfill_disable(
    mocker: MockerFixture,
) -> None:
    spy_disable = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.disable", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitDisableItem(name="example")
    object_.fulfill()

    spy_disable.assert_called_once_with()


def test_systemd_unit_disable_item_fulfill_not_disable(
    mocker: MockerFixture,
) -> None:
    spy_disable = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.disable", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_enabled",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitDisableItem(name="example")
    object_.fulfill()

    spy_disable.assert_not_called()

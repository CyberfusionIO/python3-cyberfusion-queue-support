from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_stop import (
    SystemdUnitStopItem,
)


def test_systemd_unit_stop_item_fulfill_stop(
    mocker: MockerFixture,
) -> None:
    spy_stop = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.stop", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitStopItem(name="example")
    object_.fulfill()

    spy_stop.assert_called_once_with()


def test_systemd_unit_stop_item_fulfill_not_stop(
    mocker: MockerFixture,
) -> None:
    spy_stop = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.stop", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitStopItem(name="example")
    object_.fulfill()

    spy_stop.assert_not_called()

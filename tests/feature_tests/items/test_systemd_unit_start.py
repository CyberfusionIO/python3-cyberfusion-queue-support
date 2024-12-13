from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_start import (
    SystemdUnitStartItem,
)


def test_systemd_unit_start_item_fulfill_start(
    mocker: MockerFixture,
) -> None:
    spy_start = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.start", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=False),
    )

    object_ = SystemdUnitStartItem(name="example")
    object_.fulfill()

    spy_start.assert_called_once_with()


def test_systemd_unit_start_item_fulfill_not_start(
    mocker: MockerFixture,
) -> None:
    spy_start = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.start", return_value=None
    )
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.is_active",
        new=mocker.PropertyMock(return_value=True),
    )

    object_ = SystemdUnitStartItem(name="example")
    object_.fulfill()

    spy_start.assert_not_called()

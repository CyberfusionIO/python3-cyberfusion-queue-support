from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_unit_restart import (
    SystemdUnitRestartItem,
)


def test_systemd_unit_restart_item_fulfill_restart(
    mocker: MockerFixture,
) -> None:
    spy_restart = mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.restart", return_value=None
    )

    object_ = SystemdUnitRestartItem(name="example")
    object_.fulfill()

    spy_restart.assert_called_once_with()

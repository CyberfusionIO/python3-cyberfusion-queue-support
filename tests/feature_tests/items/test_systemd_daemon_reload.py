from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_daemon_reload import (
    SystemdDaemonReloadItem,
)


def test_systemd_daemon_reload_item_fulfill_reload(
    mocker: MockerFixture,
) -> None:
    spy_reload = mocker.patch(
        "cyberfusion.SystemdSupport.manager.SystemdManager.daemon_reload",
        return_value=None,
    )

    object_ = SystemdDaemonReloadItem()
    object_.fulfill()

    spy_reload.assert_called_once_with()

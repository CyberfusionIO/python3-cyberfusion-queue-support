from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_daemon_reload import (
    SystemdDaemonReloadItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdDaemonReloadItemReloadOutcome,
)

# Equal


def test_systemd_daemon_reload_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdDaemonReloadItem() == SystemdDaemonReloadItem()


def test_systemd_daemon_reload_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdDaemonReloadItem() == 5) is False


# Outcomes


def test_systemd_daemon_reload_item_has_outcome_reload(
    existent_file_path: Generator[str, None, None], mocker: MockerFixture
) -> None:
    object_ = SystemdDaemonReloadItem()

    assert SystemdDaemonReloadItemReloadOutcome() in object_.outcomes

from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.systemd_tmp_files_create import (
    SystemdTmpFilesCreateItem,
)


def test_systemd_tmp_files_create_item_fulfill_create(
    mocker: MockerFixture,
) -> None:
    spy_create = mocker.patch(
        "cyberfusion.SystemdSupport.tmp_files.TmpFileConfigurationFile.create",
        return_value=None,
    )

    object_ = SystemdTmpFilesCreateItem(path="/tmp/example")
    object_.fulfill()

    spy_create.assert_called_once_with()

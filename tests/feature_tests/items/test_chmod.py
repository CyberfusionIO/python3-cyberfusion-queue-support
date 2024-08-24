import os
from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.chmod import ChmodItem
from cyberfusion.QueueSupport.utilities import get_decimal_permissions

MODE = 0o755


def test_chmod_item_fulfill_mode_change(
    existent_file_path: Generator[str, None, None],
) -> None:
    old_mode = get_decimal_permissions(existent_file_path)
    assert old_mode != MODE

    object_ = ChmodItem(path=existent_file_path, mode=MODE)
    object_.fulfill()

    assert get_decimal_permissions(existent_file_path) == MODE


def test_chmod_item_fulfill_not_mode_change(
    mocker: MockerFixture, existent_file_path: Generator[str, None, None]
) -> None:
    os.chmod(existent_file_path, MODE)

    spy_chmod = mocker.spy(os, "chmod")

    object_ = ChmodItem(path=existent_file_path, mode=MODE)
    object_.fulfill()

    spy_chmod.assert_not_called()

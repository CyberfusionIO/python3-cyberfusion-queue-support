import os
from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.mkdir import MkdirItem


def test_mkdir_item_fulfill_create(non_existent_path: str) -> None:
    assert not os.path.isdir(non_existent_path)

    object_ = MkdirItem(path=non_existent_path)
    object_.fulfill()

    assert os.path.isdir(non_existent_path)


def test_mkdir_item_fulfill_not_create(
    mocker: MockerFixture, existent_directory_path: Generator[str, None, None]
) -> None:
    assert os.path.isdir(existent_directory_path)

    spy_mkdir = mocker.spy(os, "mkdir")

    object_ = MkdirItem(path=existent_directory_path)
    object_.fulfill()

    spy_mkdir.assert_not_called()

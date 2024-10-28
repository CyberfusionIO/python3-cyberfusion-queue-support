import os
from typing import Generator

from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.rmtree import RmTreeItem


def test_rmtree_item_fulfill_create(
    existent_directory_path: Generator[str, None, None],
) -> None:
    assert os.path.isdir(existent_directory_path)

    object_ = RmTreeItem(path=existent_directory_path)
    object_.fulfill()

    assert not os.path.isdir(existent_directory_path)


def test_rmtree_item_fulfill_not_create(
    mocker: MockerFixture, non_existent_path: str
) -> None:
    assert not os.path.isdir(non_existent_path)

    spy_unlink = mocker.spy(os, "unlink")

    object_ = RmTreeItem(path=non_existent_path)
    object_.fulfill()

    spy_unlink.assert_not_called()
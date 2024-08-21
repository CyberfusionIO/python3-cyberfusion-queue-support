import os
from typing import Generator

import pytest
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.unlink import UnlinkItem


def test_unlink_item_fulfill_create(
    existent_file_path: Generator[str, None, None]
) -> None:
    assert os.path.exists(existent_file_path)

    object_ = UnlinkItem(path=existent_file_path)
    object_.fulfill()

    assert not os.path.exists(existent_file_path)


def test_unlink_item_fulfill_not_create(
    mocker: MockerFixture, non_existent_path: str
) -> None:
    assert not os.path.exists(non_existent_path)

    spy_unlink = mocker.spy(os, "unlink")

    object_ = UnlinkItem(path=non_existent_path)
    object_.fulfill()

    spy_unlink.assert_not_called()

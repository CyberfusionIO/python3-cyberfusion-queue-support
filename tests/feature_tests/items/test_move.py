import os
from typing import Generator

import pytest
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.move import MoveItem


def test_move_item_fulfill_move(
    non_existent_path: str, existent_file_path: Generator[str, None, None]
) -> None:
    old_contents = open(existent_file_path, "r").read()
    assert not os.path.exists(non_existent_path)

    object_ = MoveItem(
        source=existent_file_path, destination=non_existent_path
    )
    object_.fulfill()

    assert os.path.exists(non_existent_path)
    assert not os.path.exists(existent_file_path)
    assert old_contents == open(non_existent_path, "r").read()

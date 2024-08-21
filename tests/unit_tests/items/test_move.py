import os
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.move import MoveItem
from cyberfusion.QueueSupport.outcomes import MoveItemMoveOutcome

# Equal


def test_move_item_equal(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert MoveItem(
        source=existent_file_path, destination=non_existent_path
    ) == MoveItem(source=existent_file_path, destination=non_existent_path)


def test_move_item_not_equal_source(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert MoveItem(
        source=existent_file_path, destination=non_existent_path
    ) != MoveItem(
        source=existent_file_path + "-example", destination=non_existent_path
    )


def test_move_item_not_equal_destination(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert MoveItem(
        source=existent_file_path, destination=non_existent_path
    ) != MoveItem(
        source=existent_file_path, destination=non_existent_path + "-example"
    )


def test_move_item_equal_different_type(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert (
        MoveItem(source=existent_file_path, destination=non_existent_path) == 5
    ) is False


# Validation


def test_move_item_source_symlink_raises(
    existent_symlink_path: Generator[str, None, None], non_existent_path: str
) -> None:
    with pytest.raises(PathIsSymlinkError):
        MoveItem(source=existent_symlink_path, destination=non_existent_path)


def test_move_item_destination_symlink_raises(
    existent_symlink_path: Generator[str, None, None], non_existent_path: str
) -> None:
    with pytest.raises(PathIsSymlinkError):
        MoveItem(source=non_existent_path, destination=existent_symlink_path)


# Outcomes


def test_move_item_has_outcome_move(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = MoveItem(
        source=existent_file_path, destination=non_existent_path
    )

    assert (
        MoveItemMoveOutcome(
            source=existent_file_path, destination=non_existent_path
        )
        in object_.outcomes
    )

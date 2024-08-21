import os
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.chmod import ChmodItem
from cyberfusion.QueueSupport.outcomes import ChmodItemModeChangeOutcome
from cyberfusion.QueueSupport.utilities import get_decimal_permissions

MODE = 0o755

# Equal


def test_chmod_item_equal(
    existent_file_path: Generator[str, None, None]
) -> None:
    assert ChmodItem(path=existent_file_path, mode=MODE) == ChmodItem(
        path=existent_file_path, mode=MODE
    )


def test_chmod_item_not_equal_path(
    existent_file_path: Generator[str, None, None]
) -> None:
    assert ChmodItem(path=existent_file_path, mode=MODE) != ChmodItem(
        path=existent_file_path + "-example", mode=MODE
    )


def test_chmod_item_not_equal_mode(
    existent_file_path: Generator[str, None, None]
) -> None:
    assert ChmodItem(path=existent_file_path, mode=MODE) != ChmodItem(
        path=existent_file_path, mode=MODE + 1
    )


def test_chmod_item_equal_different_type(
    existent_file_path: Generator[str, None, None]
) -> None:
    assert (ChmodItem(path=existent_file_path, mode=MODE) == 5) is False


# Validation


def test_chmod_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None]
) -> None:
    with pytest.raises(PathIsSymlinkError):
        ChmodItem(path=existent_symlink_path, mode=MODE)


# Outcomes


def test_chmod_item_not_exists_has_outcome_mode_change(
    non_existent_path: str,
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = ChmodItem(path=non_existent_path, mode=MODE)

    assert object_.outcomes == [
        ChmodItemModeChangeOutcome(
            path=non_existent_path, old_mode=None, new_mode=MODE
        )
    ]


def test_chmod_item_not_same_has_outcome_mode_change(
    existent_file_path: Generator[str, None, None],
) -> None:
    old_mode = get_decimal_permissions(existent_file_path)
    assert old_mode != MODE

    object_ = ChmodItem(path=existent_file_path, mode=MODE)

    assert (
        ChmodItemModeChangeOutcome(
            path=existent_file_path, old_mode=old_mode, new_mode=MODE
        )
        in object_.outcomes
    )


def test_chmod_item_same_not_has_outcome_mode_change(
    existent_file_path: Generator[str, None, None],
) -> None:
    os.chmod(existent_file_path, MODE)

    object_ = ChmodItem(path=existent_file_path, mode=MODE)

    assert (
        ChmodItemModeChangeOutcome(
            path=existent_file_path, old_mode=MODE, new_mode=MODE
        )
        not in object_.outcomes
    )

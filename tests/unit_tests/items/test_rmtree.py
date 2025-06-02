import os
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.rmtree import RmTreeItem
from cyberfusion.QueueSupport.outcomes import RmTreeItemRemoveOutcome


# Equal


def test_rmtree_item_equal(existent_file_path: Generator[str, None, None]) -> None:
    assert RmTreeItem(path=existent_file_path) == RmTreeItem(path=existent_file_path)


def test_rmtree_item_not_equal_path(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert RmTreeItem(path=existent_file_path) != RmTreeItem(
        path=existent_file_path + "-example"
    )


def test_rmtree_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (RmTreeItem(path=existent_file_path) == 5) is False


# Validation


def test_rmtree_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None],
) -> None:
    with pytest.raises(PathIsSymlinkError):
        RmTreeItem(path=existent_symlink_path)


# Outcomes


def test_rmtree_item_exists_has_outcome_remove(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert os.path.exists(existent_file_path)

    object_ = RmTreeItem(path=existent_file_path)

    assert RmTreeItemRemoveOutcome(path=existent_file_path) in object_.outcomes


def test_rmtree_item_not_exists_not_has_outcome_remove(
    non_existent_path: str,
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = RmTreeItem(path=non_existent_path)

    assert not object_.outcomes

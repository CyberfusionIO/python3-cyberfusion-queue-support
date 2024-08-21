import os
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.mkdir import MkdirItem
from cyberfusion.QueueSupport.outcomes import MkdirItemCreateOutcome

# Equal


def test_mkdir_item_equal(
    existent_directory_path: Generator[str, None, None]
) -> None:
    assert MkdirItem(path=existent_directory_path) == MkdirItem(
        path=existent_directory_path
    )


def test_mkdir_item_not_equal_path(
    existent_directory_path: Generator[str, None, None]
) -> None:
    assert MkdirItem(path=existent_directory_path) != MkdirItem(
        path=existent_directory_path + "-example"
    )


def test_mkdir_item_equal_different_type(
    existent_directory_path: Generator[str, None, None]
) -> None:
    assert (MkdirItem(path=existent_directory_path) == 5) is False


# Validation


def test_mkdir_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None]
) -> None:
    with pytest.raises(PathIsSymlinkError):
        MkdirItem(path=existent_symlink_path)


# Outcomes


def test_mkdir_item_not_exists_has_outcome_create(
    non_existent_path: str,
) -> None:
    assert not os.path.isdir(non_existent_path)

    object_ = MkdirItem(path=non_existent_path)

    assert MkdirItemCreateOutcome(path=non_existent_path) in object_.outcomes


def test_mkdir_item_exists_not_has_outcome_create(
    existent_directory_path: Generator[str, None, None],
) -> None:
    assert os.path.isdir(existent_directory_path)

    object_ = MkdirItem(path=existent_directory_path)

    assert (
        MkdirItemCreateOutcome(path=existent_directory_path)
        not in object_.outcomes
    )

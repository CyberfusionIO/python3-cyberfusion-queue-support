import os
import uuid
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import (
    PathIsSymlinkError,
    PathIsFileError,
    ParentNotFoundError,
)
from cyberfusion.QueueSupport.items.mkdir import MkdirItem
from cyberfusion.QueueSupport.outcomes import MkdirItemCreateOutcome
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_mkdir_item_equal(existent_directory_path: Generator[str, None, None]) -> None:
    assert MkdirItem(path=existent_directory_path) == MkdirItem(
        path=existent_directory_path
    )


def test_mkdir_item_not_equal_path(
    existent_directory_path: Generator[str, None, None],
) -> None:
    assert MkdirItem(path=existent_directory_path) != MkdirItem(
        path=existent_directory_path + "-example"
    )


def test_mkdir_item_equal_different_type(
    existent_directory_path: Generator[str, None, None],
) -> None:
    assert (MkdirItem(path=existent_directory_path) == 5) is False


# Validation


def test_mkdir_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None],
) -> None:
    object_ = MkdirItem(path=existent_symlink_path)

    with pytest.raises(PathIsSymlinkError):
        object_.outcomes


def test_mkdir_item_path_file_raises(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = MkdirItem(path=existent_file_path)

    with pytest.raises(PathIsFileError):
        object_.outcomes


def test_mkdir_item_path_no_parent_raises(
    non_existent_path: Generator[str, None, None],
) -> None:
    nested_non_existent_path = os.path.join(non_existent_path, str(uuid.uuid4()))

    object_ = MkdirItem(path=nested_non_existent_path, recursively=False)

    with pytest.raises(ParentNotFoundError):
        object_.outcomes


# Outcomes


def test_mkdir_item_not_exists_has_outcome_create(
    non_existent_path: str,
) -> None:
    assert not os.path.isdir(non_existent_path)

    object_ = MkdirItem(path=non_existent_path)

    assert MkdirItemCreateOutcome(path=non_existent_path) in object_.outcomes


def test_mkdir_item_recursively_not_exists_has_outcome_create(
    non_existent_path: str,
) -> None:
    nested_non_existent_path = os.path.join(non_existent_path, str(uuid.uuid4()))

    assert not os.path.isdir(nested_non_existent_path)

    object_ = MkdirItem(path=nested_non_existent_path, recursively=True)

    assert MkdirItemCreateOutcome(path=non_existent_path) in object_.outcomes
    assert MkdirItemCreateOutcome(path=nested_non_existent_path) in object_.outcomes


def test_mkdir_item_exists_not_has_outcome_create(
    existent_directory_path: Generator[str, None, None],
) -> None:
    assert os.path.isdir(existent_directory_path)

    object_ = MkdirItem(path=existent_directory_path)

    assert not object_.outcomes


# Serialization


def test_mkdir_item_serialization(
    non_existent_path: str,
) -> None:
    object_ = MkdirItem(path=non_existent_path)

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "path": non_existent_path,
            "recursively": False,
        }
    )

    assert serialized == expected

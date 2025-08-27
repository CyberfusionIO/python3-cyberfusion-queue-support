import os
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.rmtree import RmTreeItem
from cyberfusion.QueueSupport.outcomes import RmTreeItemRemoveOutcome
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder


# Equal


def test_rmtree_item_equal(existent_file_path: Generator[str, None, None]) -> None:
    assert RmTreeItem(path=existent_file_path, min_depth=1) == RmTreeItem(
        path=existent_file_path, min_depth=1
    )


def test_rmtree_item_not_equal_path(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert RmTreeItem(path=existent_file_path, min_depth=1) != RmTreeItem(
        path=existent_file_path + "-example", min_depth=1
    )


def test_rmtree_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (RmTreeItem(path=existent_file_path, min_depth=1) == 5) is False


# Validation


def test_rmtree_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None],
) -> None:
    with pytest.raises(PathIsSymlinkError):
        RmTreeItem(path=existent_symlink_path, min_depth=1)


def test_rmtree_item_path_not_absolute() -> None:
    with pytest.raises(ValueError) as error:
        RmTreeItem(path="test", min_depth=1)

    assert error.value.args[0] == "path must be an absolute path"


def test_rmtree_item_path_min_min_depth(
    existent_file_path: Generator[str, None, None],
) -> None:
    with pytest.raises(ValueError) as error:
        RmTreeItem(path=existent_file_path, min_depth=0)

    assert error.value.args[0] == "min_depth must be greater than 0"


def test_rmtree_item_path_less_min_depth() -> None:
    with pytest.raises(ValueError) as error:
        RmTreeItem(path="/", min_depth=1)

    assert error.value.args[0] == "path doesn't have enough depth: 0 < 1"

    with pytest.raises(ValueError) as error:
        RmTreeItem(path="//", min_depth=1)

    assert error.value.args[0] == "path doesn't have enough depth: 0 < 1"

    with pytest.raises(ValueError) as error:
        RmTreeItem(path="/./", min_depth=1)

    assert error.value.args[0] == "path doesn't have enough depth: 0 < 1"

    with pytest.raises(ValueError) as error:
        RmTreeItem(path="/test/../", min_depth=1)

    assert error.value.args[0] == "path doesn't have enough depth: 0 < 1"


# Outcomes


def test_rmtree_item_exists_has_outcome_remove(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert os.path.exists(existent_file_path)

    object_ = RmTreeItem(path=existent_file_path, min_depth=1)

    assert RmTreeItemRemoveOutcome(path=existent_file_path) in object_.outcomes


def test_rmtree_item_not_exists_not_has_outcome_remove(
    non_existent_path: str,
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = RmTreeItem(path=non_existent_path, min_depth=1)

    assert not object_.outcomes


# Serialization


def test_rmtree_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = RmTreeItem(path=existent_file_path, min_depth=1)

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "path": existent_file_path,
        }
    )

    assert serialized == expected

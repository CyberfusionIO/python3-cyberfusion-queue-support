import os
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.unlink import UnlinkItem
from cyberfusion.QueueSupport.outcomes import UnlinkItemUnlinkOutcome
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_unlink_item_equal(existent_file_path: Generator[str, None, None]) -> None:
    assert UnlinkItem(path=existent_file_path) == UnlinkItem(path=existent_file_path)


def test_unlink_item_not_equal_path(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert UnlinkItem(path=existent_file_path) != UnlinkItem(
        path=existent_file_path + "-example"
    )


def test_unlink_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (UnlinkItem(path=existent_file_path) == 5) is False


# Validation


def test_unlink_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None],
) -> None:
    with pytest.raises(PathIsSymlinkError):
        UnlinkItem(path=existent_symlink_path)


# Outcomes


def test_unlink_item_exists_has_outcome_unlink(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert os.path.exists(existent_file_path)

    object_ = UnlinkItem(path=existent_file_path)

    assert UnlinkItemUnlinkOutcome(path=existent_file_path) in object_.outcomes


def test_unlink_item_not_exists_not_has_outcome_unlink(
    non_existent_path: str,
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = UnlinkItem(path=non_existent_path)

    assert not object_.outcomes


# Serialization


def test_unlink_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = UnlinkItem(path=existent_file_path)

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "path": existent_file_path,
        }
    )

    assert serialized == expected

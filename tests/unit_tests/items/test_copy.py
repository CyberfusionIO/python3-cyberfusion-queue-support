from pathlib import Path
from typing import Generator

import pytest

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.copy import CopyItem
from cyberfusion.QueueSupport.outcomes import CopyItemCopyOutcome

# Equal


def test_copy_item_equal(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert CopyItem(
        source=existent_file_path, destination=non_existent_path
    ) == CopyItem(source=existent_file_path, destination=non_existent_path)


def test_copy_item_not_equal_source(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert CopyItem(
        source=existent_file_path, destination=non_existent_path
    ) != CopyItem(source=existent_file_path + "-example", destination=non_existent_path)


def test_copy_item_not_equal_destination(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert CopyItem(
        source=existent_file_path, destination=non_existent_path
    ) != CopyItem(source=existent_file_path, destination=non_existent_path + "-example")


def test_copy_item_equal_different_type(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert (
        CopyItem(source=existent_file_path, destination=non_existent_path) == 5
    ) is False


# Validation


def test_copy_item_source_symlink_raises(
    existent_symlink_path: Generator[str, None, None], non_existent_path: str
) -> None:
    with pytest.raises(PathIsSymlinkError):
        CopyItem(source=existent_symlink_path, destination=non_existent_path)


def test_copy_item_destination_symlink_raises(
    existent_symlink_path: Generator[str, None, None], non_existent_path: str
) -> None:
    with pytest.raises(PathIsSymlinkError):
        CopyItem(source=non_existent_path, destination=existent_symlink_path)


# Outcomes


def test_copy_item_not_exists_has_outcome_copy(
    tmp_path: Path,
) -> None:
    tmp_file = tmp_path / "exists"
    tmp_file_not_exists = tmp_file / "not_exists"

    tmp_file.write_text("example")

    object_ = CopyItem(source=str(tmp_file), destination=str(tmp_file_not_exists))

    assert object_.outcomes

    outcome = object_.outcomes[0]

    assert isinstance(outcome, CopyItemCopyOutcome)
    assert outcome.source == str(tmp_file)
    assert outcome.destination == str(tmp_file_not_exists)
    assert outcome.changed_lines


def test_copy_item_not_same_has_outcome_copy(
    existent_file_path: str,
    tmp_path: Path,
) -> None:
    tmp_file = tmp_path / "example"

    tmp_file.write_text("example")

    object_ = CopyItem(source=existent_file_path, destination=str(tmp_file))

    assert object_.outcomes

    outcome = object_.outcomes[0]

    assert isinstance(outcome, CopyItemCopyOutcome)
    assert outcome.source == existent_file_path
    assert outcome.destination == str(tmp_file)
    assert outcome.changed_lines


def test_copy_item_same_not_has_outcomes(
    existent_file_path: str,
    tmp_path: Path,
) -> None:
    tmp_file = tmp_path / "example"

    tmp_file.touch()

    object_ = CopyItem(source=existent_file_path, destination=str(tmp_file))

    assert not object_.outcomes


def test_copy_item_binary_source_has_outcome_copy(
    tmp_path: Path,
) -> None:
    tmp_binary_file = tmp_path / "example"

    tmp_binary_file.write_bytes(b'\xFF')

    object_ = CopyItem(source=str(tmp_binary_file), destination=str(tmp_path / "not_exists"))

    assert object_.outcomes

    outcome = object_.outcomes[0]

    assert isinstance(outcome, CopyItemCopyOutcome)
    assert outcome.source == str(tmp_binary_file)
    assert outcome.changed_lines is None


def test_copy_item_binary_destination_has_outcome_copy(
    existent_file_path: str,
    tmp_path: Path,
) -> None:
    tmp_binary_file = tmp_path / "example"

    tmp_binary_file.write_bytes(b'\xFF')

    object_ = CopyItem(source=existent_file_path, destination=str(tmp_binary_file))

    assert object_.outcomes

    outcome = object_.outcomes[0]

    assert isinstance(outcome, CopyItemCopyOutcome)
    assert outcome.source == existent_file_path
    assert outcome.destination == str(tmp_binary_file)
    assert outcome.changed_lines is None
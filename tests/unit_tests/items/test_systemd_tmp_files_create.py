from typing import Generator

from cyberfusion.QueueSupport.items.systemd_tmp_files_create import (
    SystemdTmpFilesCreateItem,
)
from cyberfusion.QueueSupport.outcomes import (
    SystemdTmpFilesCreateItemCreateOutcome,
)
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_systemd_tmp_files_create_item_equal(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdTmpFilesCreateItem(path="/tmp/example") == SystemdTmpFilesCreateItem(
        path="/tmp/example"
    )


def test_systemd_tmp_files_create_item_not_equal_name(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert SystemdTmpFilesCreateItem(path="/tmp/example") != SystemdTmpFilesCreateItem(
        path="/tmp/example/example"
    )


def test_systemd_tmp_files_create_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
) -> None:
    assert (SystemdTmpFilesCreateItem(path="/tmp/example") == 5) is False


# Outcomes


def test_systemd_tmp_files_create_item_has_outcome_create(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdTmpFilesCreateItem(path="/tmp/example")

    assert (
        SystemdTmpFilesCreateItemCreateOutcome(path="/tmp/example") in object_.outcomes
    )


# Serialization


def test_systemd_tmp_files_create_item_serialization(
    existent_file_path: Generator[str, None, None],
) -> None:
    object_ = SystemdTmpFilesCreateItem(path="/tmp/example")

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "path": "/tmp/example",
        }
    )

    assert serialized == expected

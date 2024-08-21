import os
from typing import Generator

import pytest
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport import Queue, QueueFulfillFailed
from cyberfusion.QueueSupport.items.chmod import ChmodItem
from cyberfusion.QueueSupport.items.command import CommandItem

MODE = 0o600


def test_queue_process_raises_exception(
    queue: Queue, existent_file_path: Generator[str, None, None]
) -> None:
    item = ChmodItem(
        path=existent_file_path, mode=204983136789054  # Invalid mode
    )

    queue.add(item)

    with pytest.raises(QueueFulfillFailed) as e:
        queue.process(preview=False)

    assert e.value.item == item


def test_queue_process_not_overrides_exception(
    queue: Queue,
    existent_file_path: Generator[str, None, None],
    mocker: MockerFixture,
) -> None:
    """When QueueFulfillFailed (or subclass) is raised, don't raise a new QueueFulfillFailed exception."""
    item = CommandItem(command=["true"])  # Random item

    exception = QueueFulfillFailed(item=item)

    mocker.patch(
        "cyberfusion.QueueSupport.items.command.CommandItem.fulfill",
        side_effect=exception,
    )

    queue.add(item)

    with pytest.raises(QueueFulfillFailed) as e:
        queue.process(preview=False)

    assert e.value is exception  # Same instance = not re-raised


def test_queue_add_adds(
    queue: Queue, existent_file_path: Generator[str, None, None]
) -> None:
    item = ChmodItem(path=existent_file_path, mode=MODE)

    queue.add(item)

    assert item in queue.items


def test_queue_add_moves_duplicate(
    queue: Queue, existent_file_path: Generator[str, None, None]
) -> None:
    item_0 = ChmodItem(path=existent_file_path, mode=MODE)
    item_1 = ChmodItem(path=existent_file_path, mode=MODE + 1)

    queue.add(item_0)
    queue.add(item_1)

    assert queue.items == [item_0, item_1]

    queue.add(item_0, move_duplicate_last=True)  # Duplicate

    assert queue.items == [
        item_1,
        item_0,
    ]  # Duplicate item_0 moved to last place


def test_queue_add_not_moves_duplicate(
    queue: Queue, existent_file_path: Generator[str, None, None]
) -> None:
    item_0 = ChmodItem(path=existent_file_path, mode=MODE)
    item_1 = ChmodItem(path=existent_file_path, mode=MODE + 1)

    queue.add(item_0)
    queue.add(item_1)

    assert queue.items == [item_0, item_1]

    queue.add(item_0, move_duplicate_last=False)  # Duplicate

    assert queue.items == [
        item_0,
        item_1,
    ]  # Duplicate item_0 not moved, and not added twice


def test_queue_process_returns_outcomes_when_not_hide_outcomes(
    mocker: MockerFixture,
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    spy_chmod = mocker.spy(os, "chmod")

    queue.add(
        ChmodItem(path=existent_file_path, mode=MODE, hide_outcomes=False)
    )

    assert queue.process(preview=False)

    spy_chmod.assert_called_once_with(existent_file_path, MODE)


def test_queue_process_not_returns_outcomes_when_hide_outcomes(
    mocker: MockerFixture,
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    spy_chmod = mocker.spy(os, "chmod")

    queue.add(
        ChmodItem(path=existent_file_path, mode=MODE, hide_outcomes=True)
    )

    assert not queue.process(preview=False)

    spy_chmod.assert_called_once_with(existent_file_path, MODE)


def test_queue_process_not_preview_fulfills(
    existent_file_path: Generator[str, None, None],
    mocker: MockerFixture,
    queue: Queue,
) -> None:
    queue.add(ChmodItem(path=existent_file_path, mode=MODE))

    spy_fulfill = mocker.spy(queue.items[0].__class__, "fulfill")

    queue.process(preview=False)

    spy_fulfill.assert_called_once_with(mocker.ANY)


def test_queue_process_preview_not_fulfills(
    existent_file_path: Generator[str, None, None],
    mocker: MockerFixture,
    queue: Queue,
) -> None:
    queue.add(ChmodItem(path=existent_file_path, mode=MODE))

    spy_fulfill = mocker.spy(queue.items[0].__class__, "fulfill")

    queue.process(preview=True)

    spy_fulfill.assert_not_called()

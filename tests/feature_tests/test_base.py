import os
from copy import copy
from typing import Generator

from pytest_mock import MockerFixture
from sqlalchemy import select
from sqlalchemy.orm import Session

from cyberfusion.QueueSupport import (
    Queue,
    database,
)
from cyberfusion.QueueSupport.items.chmod import ChmodItem

MODE = 0o600


def test_init_queue_adds_database_object(
    queue: Queue,
    existent_file_path: Generator[str, None, None],
    database_session: Session,
) -> None:
    queue_objects = database_session.scalars(select(database.Queue)).all()

    assert len(queue_objects) == 1

    assert queue_objects[0].id == queue.queue_database_object.id


def test_queue_add_adds_database_object(
    queue: Queue,
    existent_file_path: Generator[str, None, None],
    database_session: Session,
    mocker: MockerFixture,
) -> None:
    queue._database_session = database_session

    item = ChmodItem(path=existent_file_path, mode=MODE)

    queue.add(item)

    database_session.commit()

    item_database_objects = database_session.scalars(select(database.QueueItem)).all()

    assert len(item_database_objects) == 1

    item_dict = copy(item.__dict__)

    del item_dict["_reference"]
    del item_dict["_hide_outcomes"]

    assert item_database_objects[0].id
    assert item_database_objects[0].queue_id == queue.queue_database_object.id
    assert item_database_objects[0].type == item.__class__.__name__
    assert item_database_objects[0].reference == item.reference
    assert item_database_objects[0].hide_outcomes == item.hide_outcomes
    assert not item_database_objects[0].deduplicated
    assert item_database_objects[0].attributes == item_dict
    assert item_database_objects[0].traceback is None


def test_queue_add_adds_mapping(
    queue: Queue,
    existent_file_path: Generator[str, None, None],
    database_session: Session,
) -> None:
    queue._database_session = database_session

    item = ChmodItem(path=existent_file_path, mode=MODE)

    queue.add(item)

    database_session.commit()

    assert len(queue.item_mappings) == 1

    item_database_objects = database_session.scalars(select(database.QueueItem)).all()

    assert len(item_database_objects) == 1

    assert queue.item_mappings[0].item == item
    assert queue.item_mappings[0].database_object.id == item_database_objects[0].id


def test_queue_add_run_duplicate_last(
    queue: Queue, existent_file_path: Generator[str, None, None]
) -> None:
    item_0 = ChmodItem(path=existent_file_path, mode=MODE)
    item_1 = ChmodItem(path=existent_file_path, mode=MODE + 1)

    queue.add(item_0)
    queue.add(item_1)

    assert [item_mapping.item for item_mapping in queue.item_mappings] == [
        item_0,
        item_1,
    ]

    queue.add(item_0, run_duplicate_last=True)  # Duplicate

    assert [item_mapping.item for item_mapping in queue.item_mappings] == [
        item_0,
        item_1,
        item_0,
    ]

    assert [
        item_mapping.item
        for item_mapping in queue.item_mappings
        if not item_mapping.database_object.deduplicated
    ] == [
        item_1,
        item_0,
    ]  # item_0 is last

    assert [
        item_mapping.item
        for item_mapping in queue.item_mappings
        if item_mapping.database_object.deduplicated
    ] == [item_0]


def test_queue_add_not_run_duplicate_last(
    queue: Queue, existent_file_path: Generator[str, None, None]
) -> None:
    item_0 = ChmodItem(path=existent_file_path, mode=MODE)
    item_1 = ChmodItem(path=existent_file_path, mode=MODE + 1)

    queue.add(item_0)
    queue.add(item_1)

    assert [item_mapping.item for item_mapping in queue.item_mappings] == [
        item_0,
        item_1,
    ]

    queue.add(item_0, run_duplicate_last=False)  # Duplicate

    assert [item_mapping.item for item_mapping in queue.item_mappings] == [
        item_0,
        item_1,
        item_0,
    ]

    assert [
        item_mapping.item
        for item_mapping in queue.item_mappings
        if not item_mapping.database_object.deduplicated
    ] == [
        item_0,
        item_1,
    ]  # item_0 is first

    assert [
        item_mapping.item
        for item_mapping in queue.item_mappings
        if item_mapping.database_object.deduplicated
    ] == [item_0]


def test_queue_process_adds_database_object(
    queue: Queue, database_session: Session
) -> None:
    queue.process(preview=False)

    process_database_objects = database_session.scalars(
        select(database.QueueProcess)
    ).all()

    assert len(process_database_objects) == 1

    assert process_database_objects[0].queue_id == queue.queue_database_object.id
    assert not process_database_objects[0].preview


def test_queue_process_returns_outcomes_when_not_hide_outcomes(
    mocker: MockerFixture,
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    spy_chmod = mocker.spy(os, "chmod")

    queue.add(ChmodItem(path=existent_file_path, mode=MODE, hide_outcomes=False))

    assert queue.process(preview=False)

    spy_chmod.assert_called_once_with(existent_file_path, MODE)


def test_queue_process_not_returns_outcomes_when_hide_outcomes(
    mocker: MockerFixture,
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    spy_chmod = mocker.spy(os, "chmod")

    queue.add(ChmodItem(path=existent_file_path, mode=MODE, hide_outcomes=True))

    assert not queue.process(preview=False)

    spy_chmod.assert_called_once_with(existent_file_path, MODE)


def test_queue_process_preview_returns_outcomes_when_not_hide_outcomes(
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    queue.add(ChmodItem(path=existent_file_path, mode=MODE, hide_outcomes=False))

    assert queue.process(preview=True)


def test_queue_preview_not_returns_outcomes_when_hide_outcomes(
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    queue.add(ChmodItem(path=existent_file_path, mode=MODE, hide_outcomes=True))

    assert not queue.process(preview=True)


def test_queue_process_not_returns_outcomes_deduplicated(
    queue: Queue,
    existent_file_path: Generator[str, None, None],
    database_session: Session,
) -> None:
    item_0_deduplicated = ChmodItem(
        reference="deduplicated", path=existent_file_path, mode=MODE
    )
    item_0 = ChmodItem(reference="not_deduplicated", path=existent_file_path, mode=MODE)

    queue.add(item_0_deduplicated)
    queue.add(item_0, run_duplicate_last=True)

    queue.process(preview=False)

    outcome_database_objects = database_session.scalars(
        select(database.QueueItemOutcome)
    ).all()

    assert (
        len(
            [
                outcome_database_object
                for outcome_database_object in outcome_database_objects
                if outcome_database_object.queue_item.reference != item_0.reference
            ]
        )
        == 0
    )


def test_queue_process_not_preview_fulfills(
    existent_file_path: Generator[str, None, None],
    mocker: MockerFixture,
    queue: Queue,
) -> None:
    queue.add(ChmodItem(path=existent_file_path, mode=MODE))

    spy_fulfill = mocker.spy(queue.item_mappings[0].item.__class__, "fulfill")

    queue.process(preview=False)

    spy_fulfill.assert_called_once_with(mocker.ANY)


def test_queue_process_preview_not_fulfills(
    existent_file_path: Generator[str, None, None],
    mocker: MockerFixture,
    queue: Queue,
) -> None:
    queue.add(ChmodItem(path=existent_file_path, mode=MODE))

    spy_fulfill = mocker.spy(queue.item_mappings[0].item.__class__, "fulfill")

    queue.process(preview=True)

    spy_fulfill.assert_not_called()


def test_queue_process_adds_outcomes_database_object(
    queue: Queue,
    existent_file_path: Generator[str, None, None],
    database_session: Session,
) -> None:
    item = ChmodItem(path=existent_file_path, mode=MODE)

    queue.add(item)

    outcomes = queue.process(preview=False)

    outcome_database_objects = database_session.scalars(
        select(database.QueueItemOutcome)
    ).all()

    assert len(outcome_database_objects) == 1

    assert (
        outcome_database_objects[0].queue_item_id
        == queue.item_mappings[0].database_object.id
    )
    assert outcome_database_objects[0].queue_process_id
    assert outcome_database_objects[0].queue_process
    assert outcome_database_objects[0].type == outcomes[0].__class__.__name__
    assert outcome_database_objects[0].attributes == outcomes[0].__dict__
    assert outcome_database_objects[0].string == str(outcomes[0])


def test_queue_process_traceback(
    database_session: Session,
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    item = ChmodItem(
        path=existent_file_path,
        mode=204983136789054,  # Invalid mode
    )

    queue.add(item)

    queue.process(preview=False)

    item_database_objects = database_session.scalars(select(database.QueueItem)).all()

    assert len(item_database_objects) == 1

    assert "Traceback (most recent call last):" in item_database_objects[0].traceback


def test_queue_process_no_fulfill_after_traceback(
    mocker: MockerFixture,
    database_session: Session,
    existent_file_path: Generator[str, None, None],
    queue: Queue,
) -> None:
    """Test that when an item has a traceback (i.e. fulfilling failed), other items are not fulfilled."""
    item_1 = ChmodItem(
        path=existent_file_path,
        mode=204983136789054,  # Invalid mode
    )

    item_2 = item_1.__class__(
        path=existent_file_path,
        mode=MODE,
    )

    spy_fulfill = mocker.spy(item_1.__class__, "fulfill")

    queue.add(item_1)
    queue.add(item_2)

    queue.process(preview=False)

    item_database_objects = database_session.scalars(select(database.QueueItem)).all()

    assert len(item_database_objects) == 2

    assert "Traceback (most recent call last):" in item_database_objects[0].traceback

    spy_fulfill.assert_called_once()

import datetime
import faker
from typing import Callable

from sqlalchemy.orm import Session

from cyberfusion.QueueSupport import database, Queue
from cyberfusion.QueueSupport.scripts import purge_queues
from cyberfusion.QueueSupport.settings import settings


def test_main(
    database_session: Session, queue_generator: Callable[[], Queue], faker: faker.Faker
) -> None:
    keep_queue = queue_generator()
    purge_queue = queue_generator()

    keep_queue_database_object = database_session.get(
        database.Queue, keep_queue.queue_database_object.id
    )
    purge_queue_database_object = database_session.get(
        database.Queue, purge_queue.queue_database_object.id
    )

    keep_queue_database_object.created_at = faker.date_between_dates(
        date_start=datetime.datetime.now()
        - datetime.timedelta(days=settings.queue_purge_days),
        date_end=datetime.datetime.now(),
    )
    purge_queue_database_object.created_at = faker.date_between(
        end_date=datetime.datetime.now()
        - datetime.timedelta(days=settings.queue_purge_days)
    )

    database_session.add(keep_queue_database_object)
    database_session.add(purge_queue_database_object)

    database_session.commit()

    assert database_session.query(database.Queue).count() == 2

    purge_queues.main()

    queues = database_session.query(database.Queue).all()

    assert len(queues) == 1

    assert queues[0].id == keep_queue_database_object.id

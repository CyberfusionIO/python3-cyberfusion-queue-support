from typing import Optional

from cyberfusion.SystemdSupport import Unit
from sqlalchemy.orm import Session

from cyberfusion.QueueSupport import Queue
from tests.stubs import NoopItemStub


def test_add_unit_attribute_database(
    queue: Queue, test_database_session: Session
) -> None:
    NAME = "example"

    class UnitItem(NoopItemStub):
        def __init__(
            self,
            *,
            name: str,
            reference: Optional[str] = None,
            hide_outcomes: bool = False,
        ) -> None:
            """Set attributes."""
            self.name = name
            self._reference = reference
            self._hide_outcomes = hide_outcomes

            self.unit = Unit(self.name)

    item = UnitItem(name=NAME)

    queue.add(item)

    assert queue.item_mappings[0].database_object.attributes["unit"] == {"name": NAME}

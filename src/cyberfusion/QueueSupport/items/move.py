"""Item."""

import logging
import os
import shutil
from typing import List, Optional

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.interfaces import OutcomeInterface
from cyberfusion.QueueSupport.items import _Item
from cyberfusion.QueueSupport.outcomes import MoveItemMoveOutcome

logger = logging.getLogger(__name__)


class MoveItem(_Item):
    """Represents item."""

    def __init__(
        self,
        *,
        source: str,
        destination: str,
        reference: Optional[str] = None,
        hide_outcomes: bool = False,
    ) -> None:
        """Set attributes."""
        self.source = source
        self.destination = destination
        self._reference = reference
        self._hide_outcomes = hide_outcomes

        if os.path.islink(self.source):
            raise PathIsSymlinkError(self.source)

        if os.path.islink(self.destination):
            raise PathIsSymlinkError(self.destination)

    @property
    def outcomes(self) -> List[OutcomeInterface]:
        """Get outcomes of calling self.fulfill."""
        outcomes = []

        outcomes.append(
            MoveItemMoveOutcome(
                source=self.source, destination=self.destination
            )
        )

        return outcomes

    def fulfill(self) -> None:
        """Fulfill outcomes."""
        move_outcomes = [
            x for x in self.outcomes if isinstance(x, MoveItemMoveOutcome)
        ]

        shutil.move(move_outcomes[0].source, move_outcomes[0].destination)

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, MoveItem):
            return False

        return (
            other.source == self.source
            and other.destination == self.destination
        )
"""Item."""

import logging
from typing import List, Optional

from cyberfusion.QueueSupport.interfaces import OutcomeInterface
from cyberfusion.QueueSupport.items import _Item
from cyberfusion.QueueSupport.outcomes import (
    SystemdUnitRestartItemRestartOutcome,
)
from cyberfusion.SystemdSupport.units import Unit

logger = logging.getLogger(__name__)


class SystemdUnitRestartItem(_Item):
    """Represents item."""

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

    @property
    def outcomes(self) -> List[OutcomeInterface]:
        """Get outcomes of calling self.fulfill."""
        outcomes = []

        outcomes.append(SystemdUnitRestartItemRestartOutcome(unit=self.unit))

        return outcomes

    def fulfill(self) -> None:
        """Fulfill outcomes."""
        systemd_unit_restart_outcomes = [
            x
            for x in self.outcomes
            if isinstance(x, SystemdUnitRestartItemRestartOutcome)
        ]

        systemd_unit_restart_outcomes[0].unit.restart()

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, SystemdUnitRestartItem):
            return False

        return other.name == self.name
"""Item."""

import logging
import subprocess
from typing import List, Optional

from cyberfusion.QueueSupport.exceptions import CommandQueueFulfillFailed
from cyberfusion.QueueSupport.interfaces import OutcomeInterface
from cyberfusion.QueueSupport.items import _Item
from cyberfusion.QueueSupport.outcomes import CommandItemRunOutcome

logger = logging.getLogger(__name__)


class CommandItem(_Item):
    """Represents item."""

    def __init__(
        self,
        *,
        command: List[str],
        reference: Optional[str] = None,
        hide_outcomes: bool = False,
    ) -> None:
        """Set attributes."""
        self.command = command
        self._reference = reference
        self._hide_outcomes = hide_outcomes

    @property
    def outcomes(self) -> List[OutcomeInterface]:
        """Get outcomes of calling self.fulfill."""
        outcomes = []

        outcomes.append(CommandItemRunOutcome(command=self.command))

        return outcomes

    def fulfill(self) -> None:
        """Fulfill outcomes."""
        run_outcomes = [
            x for x in self.outcomes if isinstance(x, CommandItemRunOutcome)
        ]

        command = run_outcomes[0].command

        try:
            output = subprocess.run(
                command,
                check=True,
                text=True,
                capture_output=True,
            )

            logger.info("Command stdout: %s", output.stdout)
            logger.info("Command stderr: %s", output.stderr)
        except subprocess.CalledProcessError as e:
            raise CommandQueueFulfillFailed(
                self, command=command, stdout=e.stdout, stderr=e.stderr
            ) from e

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, CommandItem):
            return False

        return other.command == self.command
"""Item."""

import difflib
import logging
import os
import shutil
from typing import List, Optional

from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items import _Item
from cyberfusion.QueueSupport.outcomes import CopyItemCopyOutcome

logger = logging.getLogger(__name__)


class CopyItem(_Item):
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

    def _get_changed_lines(self) -> List[str]:
        """Get differences with destination file.

        No differences are returned when contents is not string.
        """
        changed_lines = []

        contents = []

        if os.path.isfile(self.destination):
            contents = open(self.destination).readlines()

        source_contents = open(self.source).readlines()

        for line in difflib.unified_diff(
            contents,
            source_contents,
            fromfile=self.source,
            tofile=self.destination,
            lineterm="",
            n=0,
        ):
            changed_lines.append(line)

        return changed_lines

    @property
    def outcomes(self) -> List[CopyItemCopyOutcome]:
        """Get outcomes of item."""
        outcomes = []

        changed_lines = self._get_changed_lines()

        if not os.path.exists(self.destination) or changed_lines:
            outcomes.append(
                CopyItemCopyOutcome(
                    source=self.source,
                    destination=self.destination,
                    changed_lines=changed_lines,
                )
            )

        return outcomes

    def fulfill(self) -> None:
        """Fulfill outcomes."""
        for outcome in self.outcomes:
            shutil.copyfile(outcome.source, outcome.destination)

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, CopyItem):
            return False

        return other.source == self.source and other.destination == self.destination

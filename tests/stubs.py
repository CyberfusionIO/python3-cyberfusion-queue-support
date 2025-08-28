from typing import List, Optional

from cyberfusion.QueueSupport import OutcomeInterface
from cyberfusion.QueueSupport.items import _Item


class NoopOutcome(OutcomeInterface):
    def __init__(
        self,
    ) -> None:
        pass

    def __str__(self) -> str:
        return "NOOP"

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, NoopOutcome):
            return False

        return True


class NoopItem(_Item):
    def __init__(
        self,
        *,
        reference: Optional[str] = None,
        hide_outcomes: bool = False,
        fail_silently: bool = False,
    ) -> None:
        """Set attributes."""
        self._reference = reference
        self._hide_outcomes = hide_outcomes
        self._fail_silently = fail_silently

    @property
    def outcomes(self) -> List[NoopOutcome]:
        """Get outcomes of item."""
        return [NoopOutcome()]

    def fulfill(self) -> List[NoopOutcome]:
        """Fulfill outcomes."""
        return self.outcomes

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, NoopItem):
            return False

        return True

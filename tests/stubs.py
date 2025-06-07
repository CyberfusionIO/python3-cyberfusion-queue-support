from typing import Literal

from cyberfusion.QueueSupport import _Item


class NoopItemStub(_Item):
    """Represents item."""

    @property
    def outcomes(
        self,
    ) -> Literal[[]]:
        """Get outcomes of item."""
        return []

    def fulfill(self) -> Literal[[]]:
        """Fulfill outcomes."""
        return []

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        return False

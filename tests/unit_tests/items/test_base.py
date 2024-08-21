from typing import Generator

from cyberfusion.QueueSupport.items.chmod import ChmodItem

MODE = 0o755


def test_item_reference(
    existent_file_path: Generator[str, None, None]
) -> None:
    REFERENCE = "test"

    assert (
        ChmodItem(
            path=existent_file_path, mode=0o755, reference=REFERENCE
        ).reference
        == REFERENCE
    )

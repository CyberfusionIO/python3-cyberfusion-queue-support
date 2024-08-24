import os
from typing import Generator


from cyberfusion.QueueSupport.items.copy import CopyItem


def test_copy_item_fulfill_copy(
    non_existent_path: str, existent_file_path: Generator[str, None, None]
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = CopyItem(source=existent_file_path, destination=non_existent_path)
    object_.fulfill()

    assert os.path.exists(non_existent_path)
    assert open(non_existent_path, "r").read() == open(existent_file_path, "r").read()

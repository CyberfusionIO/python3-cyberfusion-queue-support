import os
from typing import Generator

from cyberfusion.QueueSupport.utilities import get_decimal_permissions


def test_get_decimal_permissions(existent_file_path: Generator[str, None, None]):
    mode = 0o644

    os.chmod(existent_file_path, mode)

    assert get_decimal_permissions(existent_file_path) == mode

import grp
import os
import pwd
import shutil
import uuid
from pathlib import Path
from typing import Generator

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from cyberfusion.QueueSupport import Queue


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--ci", action="store_true", default=False)


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "ci")


def pytest_collection_modifyitems(config: Config, items: list) -> None:
    if config.getoption("--ci"):
        return

    for item in items:
        if "ci" not in item.keywords:
            continue

        item.add_marker(
            pytest.mark.skip(
                reason="CI only. For example, tests may require chowning to another user, which is usually not possible when running on a local system."
            )
        )


def get_path() -> str:
    """Get path.

    Path is in home directory. This is needed because on macOS, files created
    in /tmp/ are owned by the 'wheel' group, which has GID 0. For several tests,
    this causes unexpected results when they expect that a regular file is owned
    by the creating user.
    """
    return os.path.join(Path.home(), str(uuid.uuid4()))


@pytest.fixture
def queue() -> Queue:
    return Queue()


@pytest.fixture
def ci_owner_name() -> str:
    return "ci"


@pytest.fixture
def ci_group_name() -> str:
    return "ci"


@pytest.fixture
def non_existent_path() -> str:
    return get_path()


@pytest.fixture
def existent_symlink_path() -> Generator[str, None, None]:
    path = get_path()

    os.symlink(os.devnull, path)

    yield path

    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def existent_file_path() -> Generator[str, None, None]:
    path = get_path()

    with open(path, "w"):
        pass

    yield path

    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def existent_directory_path() -> Generator[str, None, None]:
    path = get_path()

    os.mkdir(path)

    yield path

    shutil.rmtree(path)


@pytest.fixture
def non_existent_uid() -> int:
    seen_uids = [user.pw_uid for user in pwd.getpwall()]

    for uid in range(1000, 60000):
        if uid in seen_uids:
            continue

        return uid

    raise Exception("Could not find free UID")


@pytest.fixture
def non_existent_gid() -> int:
    seen_gids = [group.gr_gid for group in grp.getgrall()]

    for gid in range(1000, 60000):
        if gid in seen_gids:
            continue

        return gid

    raise Exception("Could not find free GID")

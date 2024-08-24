import os
from grp import getgrgid
from pwd import getpwuid
from typing import Generator

import pytest
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.chown import ChownItem


@pytest.mark.ci
def test_chown_item_fulfill_owner_name_change(
    existent_file_path: Generator[str, None, None], ci_owner_name: str
) -> None:
    old_owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name
    assert old_owner_name != ci_owner_name
    group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=group_name,
    )
    object_.fulfill()

    assert getpwuid(os.stat(existent_file_path).st_uid).pw_name == ci_owner_name


def test_chown_item_fulfill_not_owner_name_change(
    mocker: MockerFixture,
    existent_file_path: Generator[str, None, None],
) -> None:
    spy_chown = mocker.spy(os, "chown")

    old_owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name
    old_group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=old_owner_name,
        group_name=old_group_name,
    )
    object_.fulfill()

    spy_chown.assert_not_called()


@pytest.mark.ci
def test_chown_item_fulfill_group_name_change(
    existent_file_path: Generator[str, None, None], ci_group_name: str
) -> None:
    old_group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name
    assert old_group_name != ci_group_name
    owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=owner_name,
        group_name=ci_group_name,
    )
    object_.fulfill()

    assert getgrgid(os.stat(existent_file_path).st_gid).gr_name == ci_group_name


def test_chown_item_fulfill_not_group_name_change(
    mocker: MockerFixture,
    existent_file_path: Generator[str, None, None],
) -> None:
    spy_chown = mocker.spy(os, "chown")

    old_owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name
    old_group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=old_owner_name,
        group_name=old_group_name,
    )
    object_.fulfill()

    spy_chown.assert_not_called()

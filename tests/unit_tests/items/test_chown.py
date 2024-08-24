import os
from grp import getgrgid
from pwd import getpwuid
from typing import Generator

import pytest

from cyberfusion.Common import generate_random_string
from cyberfusion.QueueSupport.exceptions import PathIsSymlinkError
from cyberfusion.QueueSupport.items.chown import ChownItem
from cyberfusion.QueueSupport.outcomes import (
    ChownItemGroupChangeOutcome,
    ChownItemOwnerChangeOutcome,
)

# Equal


def test_chown_item_equal(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    assert ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    ) == ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    )


def test_chown_item_not_equal_path(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    assert ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    ) != ChownItem(
        path=existent_file_path + "-example",
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    )


def test_chown_item_not_equal_owner_name(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    assert ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    ) != ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name + generate_random_string(),
        group_name=ci_group_name,
    )


def test_chown_item_not_equal_group_name(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    assert ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    ) != ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name + generate_random_string(),
    )


def test_chown_item_equal_different_type(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    assert (
        ChownItem(
            path=existent_file_path,
            owner_name=ci_owner_name,
            group_name=ci_group_name,
        )
        == 5
    ) is False


# Validation


def test_chown_item_path_symlink_raises(
    existent_symlink_path: Generator[str, None, None],
) -> None:
    with pytest.raises(PathIsSymlinkError):
        ChownItem(path=existent_symlink_path, owner_name=0, group_name=0)


# Outcomes: owner name


def test_chown_item_not_exists_has_outcome_owner_name_change(
    non_existent_path: str, ci_owner_name: str, ci_group_name: str
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = ChownItem(
        path=non_existent_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    )

    assert (
        ChownItemOwnerChangeOutcome(
            path=non_existent_path,
            old_owner_name=None,
            new_owner_name=ci_owner_name,
        )
        in object_.outcomes
    )


def test_chown_item_not_same_has_outcome_owner_name_change(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    old_owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name
    assert old_owner_name != ci_owner_name
    group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=group_name,
    )

    assert (
        ChownItemOwnerChangeOutcome(
            path=existent_file_path,
            old_owner_name=old_owner_name,
            new_owner_name=ci_owner_name,
        )
        in object_.outcomes
    )


def test_chown_item_same_not_has_outcome_owner_name_change(
    existent_file_path: Generator[str, None, None],
) -> None:
    old_owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name
    old_group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=old_owner_name,
        group_name=old_group_name,
    )

    assert (
        ChownItemOwnerChangeOutcome(
            path=existent_file_path,
            old_owner_name=old_owner_name,
            new_owner_name=old_group_name,
        )
        not in object_.outcomes
    )


@pytest.mark.ci
def test_chown_item_old_not_exists_has_outcome_owner_name_change(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
    non_existent_uid: int,
) -> None:
    os.chown(existent_file_path, uid=non_existent_uid, gid=-1)

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    )

    outcome = [
        outcome
        for outcome in object_.outcomes
        if isinstance(outcome, ChownItemOwnerChangeOutcome)
    ][0]
    assert outcome.old_owner_name == "(no user with UID exists)"


# Outcomes: group name


def test_chown_item_not_exists_has_outcome_group_name_change(
    non_existent_path: str, ci_owner_name: str, ci_group_name: str
) -> None:
    assert not os.path.exists(non_existent_path)

    object_ = ChownItem(
        path=non_existent_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    )

    assert (
        ChownItemGroupChangeOutcome(
            path=non_existent_path,
            old_group_name=None,
            new_group_name=ci_group_name,
        )
        in object_.outcomes
    )


def test_chown_item_not_same_has_outcome_group_name_change(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    old_group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name
    assert old_group_name != ci_group_name
    owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=owner_name,
        group_name=ci_group_name,
    )

    assert (
        ChownItemGroupChangeOutcome(
            path=existent_file_path,
            old_group_name=old_group_name,
            new_group_name=ci_group_name,
        )
        in object_.outcomes
    )


def test_chown_item_same_not_has_outcome_group_name_change(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
) -> None:
    old_owner_name = getpwuid(os.stat(existent_file_path).st_uid).pw_name
    old_group_name = getgrgid(os.stat(existent_file_path).st_gid).gr_name

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=old_owner_name,
        group_name=old_group_name,
    )

    assert (
        ChownItemGroupChangeOutcome(
            path=existent_file_path,
            old_group_name=old_owner_name,
            new_group_name=old_group_name,
        )
        not in object_.outcomes
    )


@pytest.mark.ci
def test_chown_item_old_not_exists_has_outcome_group_name_change(
    existent_file_path: Generator[str, None, None],
    ci_owner_name: str,
    ci_group_name: str,
    non_existent_gid: int,
) -> None:
    os.chown(existent_file_path, gid=non_existent_gid, uid=-1)

    object_ = ChownItem(
        path=existent_file_path,
        owner_name=ci_owner_name,
        group_name=ci_group_name,
    )

    outcome = [
        outcome
        for outcome in object_.outcomes
        if isinstance(outcome, ChownItemGroupChangeOutcome)
    ][0]
    assert outcome.old_group_name == "(no group with GID exists)"

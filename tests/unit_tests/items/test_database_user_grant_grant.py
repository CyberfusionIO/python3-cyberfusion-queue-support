from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.database_user_grant_grant import (
    DatabaseUserGrantGrantItem,
)
from cyberfusion.QueueSupport.outcomes import DatabaseUserGrantGrantItemGrantOutcome

MODE = 0o755

# Equal


def test_database_user_grant_grant_item_equal() -> None:
    assert DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name="example",
    ) == DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name="example",
    )


def test_database_user_grant_grant_item_not_equal_database_name() -> None:
    assert DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    ) != DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="test",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    )


def test_database_user_grant_grant_item_not_equal_database_user_name() -> None:
    assert DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    ) != DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="test",
        privilege_names=["ALL"],
        table_name=None,
    )


def test_database_user_grant_grant_item_not_equal_database_user_host() -> None:
    assert DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        database_user_host="example",
        privilege_names=["ALL"],
        table_name=None,
    ) != DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        database_user_host="test",
        privilege_names=["ALL"],
        table_name=None,
    )


def test_database_user_grant_grant_item_not_equal_privileges_names() -> None:
    assert DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    ) != DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["SELECT"],
        table_name=None,
    )


def test_database_user_grant_grant_item_not_equal_table_name() -> None:
    assert DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    ) != DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name="example",
    )


def test_database_user_grant_grant_item_not_equal_different_type() -> None:
    assert (
        DatabaseUserGrantGrantItem(
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            database_name="example",
            database_user_name="example",
            privilege_names=["ALL"],
            table_name=None,
        )
        == 5
    ) is False


# Outcomes


def test_database_user_grant_grant_item_not_exists_has_outcome_grant(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=False)
    )

    assert object_.outcomes == [
        DatabaseUserGrantGrantItemGrantOutcome(
            database_user_grant=object_.database_user_grant
        )
    ]


def test_database_user_grant_grant_item_exists_not_has_outcome_grant(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table_name=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=True)
    )

    assert not object_.outcomes

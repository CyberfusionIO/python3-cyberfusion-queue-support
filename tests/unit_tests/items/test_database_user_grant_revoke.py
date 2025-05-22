from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant
from pytest_mock import MockerFixture
from sqlalchemy import Table, MetaData

from cyberfusion.QueueSupport.items.database_user_grant_revoke import (
    DatabaseUserGrantRevokeItem,
)
from cyberfusion.QueueSupport.outcomes import DatabaseUserGrantRevokeItemRevokeOutcome

MODE = 0o755

# Equal


def test_database_user_grant_revoke_item_equal() -> None:
    assert DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=Table("example", MetaData()),
    ) == DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=Table("example", MetaData()),
    )


def test_database_user_grant_revoke_item_not_equal_database_name() -> None:
    assert DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    ) != DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="test",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    )


def test_database_user_grant_revoke_item_not_equal_database_user_name() -> None:
    assert DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    ) != DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="test",
        privilege_names=["ALL"],
        table=None,
    )


def test_database_user_grant_revoke_item_not_equal_database_user_host() -> None:
    assert DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        database_user_host="example",
        privilege_names=["ALL"],
        table=None,
    ) != DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        database_user_host="test",
        privilege_names=["ALL"],
        table=None,
    )


def test_database_user_grant_revoke_item_not_equal_privileges_names() -> None:
    assert DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    ) != DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["SELECT"],
        table=None,
    )


def test_database_user_grant_revoke_item_not_equal_table() -> None:
    assert DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    ) != DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=Table("example", MetaData()),
    )


def test_database_user_grant_revoke_item_not_equal_different_type() -> None:
    assert (
        DatabaseUserGrantRevokeItem(
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            database_name="example",
            database_user_name="example",
            privilege_names=["ALL"],
            table=None,
        )
        == 5
    ) is False


# Outcomes


def test_database_user_grant_revoke_item_exists_has_outcome_revoke(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=True)
    )

    assert object_.outcomes == [
        DatabaseUserGrantRevokeItemRevokeOutcome(
            database_user_grant=object_.database_user_grant
        )
    ]


def test_database_user_grant_revoke_item_not_exists_not_has_outcome_revoke(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="example",
        database_user_name="example",
        privilege_names=["ALL"],
        table=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=False)
    )

    assert object_.outcomes == []

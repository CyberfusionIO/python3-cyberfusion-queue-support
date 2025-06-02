from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_users import DatabaseUser
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.database_user_drop import (
    DatabaseUserDropItem,
)
from cyberfusion.QueueSupport.outcomes import DatabaseUserDropItemDropOutcome

MODE = 0o755

# Equal


def test_database_user_drop_item_equal() -> None:
    assert DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) == DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )


def test_database_user_drop_item_not_equal_server_software_name() -> None:
    assert DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) != DatabaseUserDropItem(
        server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
        name="example",
    )


def test_database_user_drop_item_not_equal_name() -> None:
    assert DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) != DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
    )


def test_database_user_drop_item_not_equal_host() -> None:
    assert DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        host="example",
    ) != DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        host="test",
    )


def test_database_user_drop_item_not_equal_different_type() -> None:
    assert (
        DatabaseUserDropItem(
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="example",
        )
        == 5
    ) is False


# Outcomes


def test_database_user_drop_item_exists_has_outcome_drop(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=True))

    assert object_.outcomes == [
        DatabaseUserDropItemDropOutcome(database_user=object_.database_user)
    ]


def test_database_user_drop_item_not_exists_different_password_not_has_outcome_drop(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=False))
    mocker.patch.object(object_.database_user, "_get_password", return_value="test")

    assert not object_.outcomes

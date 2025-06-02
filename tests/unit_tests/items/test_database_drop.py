from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.databases import Database
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.database_drop import DatabaseDropItem
from cyberfusion.QueueSupport.outcomes import DatabaseDropItemDropOutcome

MODE = 0o755

# Equal


def test_database_drop_item_equal() -> None:
    assert DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) == DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )


def test_database_drop_item_not_equal_server_software_name() -> None:
    assert DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) != DatabaseDropItem(
        server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
        name="example",
    )


def test_database_drop_item_not_equal_name() -> None:
    assert DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) != DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME, name="test"
    )


def test_database_drop_item_not_equal_different_type() -> None:
    assert (
        DatabaseDropItem(
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="example",
        )
        == 5
    ) is False


# Outcomes


def test_database_drop_item_exists_has_outcome_drop(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=True))

    assert object_.outcomes == [DatabaseDropItemDropOutcome(database=object_.database)]


def test_database_drop_item_not_exists_not_has_outcome_drop(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=False))

    assert object_.outcomes == []

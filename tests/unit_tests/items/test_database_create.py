from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.databases import Database
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.database_create import DatabaseCreateItem
from cyberfusion.QueueSupport.outcomes import DatabaseCreateItemCreateOutcome

MODE = 0o755

# Equal


def test_database_create_item_equal() -> None:
    assert DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) == DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )


def test_database_create_item_not_equal_server_software_name() -> None:
    assert DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) != DatabaseCreateItem(
        server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
        name="example",
    )


def test_database_create_item_not_equal_name() -> None:
    assert DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    ) != DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME, name="test"
    )


def test_database_create_item_not_equal_different_type() -> None:
    assert (
        DatabaseCreateItem(
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="example",
        )
        == 5
    ) is False


# Outcomes


def test_database_create_item_not_exists_has_outcome_create(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=False))

    assert object_.outcomes == [
        DatabaseCreateItemCreateOutcome(database=object_.database)
    ]


def test_database_create_item_exists_not_has_outcome_create(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=True))

    assert object_.outcomes == []

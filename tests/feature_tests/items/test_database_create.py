from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.databases import Database

from cyberfusion.QueueSupport.items.database_create import DatabaseCreateItem
from pytest_mock import MockerFixture


MODE = 0o755


def test_database_create_item_fulfill_create(mocker: MockerFixture) -> None:
    object_ = DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME, name="test"
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=False))
    mock = mocker.patch.object(Database, "create", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_create_item_fulfill_not_create(mocker: MockerFixture) -> None:
    object_ = DatabaseCreateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME, name="test"
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=True))

    spy_create = mocker.spy(object_.database, "create")

    object_.fulfill()

    spy_create.assert_not_called()

from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.databases import Database

from cyberfusion.QueueSupport.items.database_drop import DatabaseDropItem
from pytest_mock import MockerFixture


MODE = 0o755


def test_database_drop_item_fulfill_drop(mocker: MockerFixture) -> None:
    object_ = DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME, name="test"
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=True))
    mock = mocker.patch.object(Database, "drop", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_drop_item_fulfill_not_drop(mocker: MockerFixture) -> None:
    object_ = DatabaseDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME, name="test"
    )

    mocker.patch.object(Database, "exists", new=PropertyMock(return_value=False))

    spy_drop = mocker.spy(object_.database, "drop")

    object_.fulfill()

    spy_drop.assert_not_called()

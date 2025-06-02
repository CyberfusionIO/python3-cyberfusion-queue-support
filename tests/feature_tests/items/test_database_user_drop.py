from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_users import DatabaseUser

from cyberfusion.QueueSupport.items.database_user_drop import (
    DatabaseUserDropItem,
)
from pytest_mock import MockerFixture


MODE = 0o755


def test_database_user_drop_item_fulfill_drop(mocker: MockerFixture) -> None:
    object_ = DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=True))
    mock = mocker.patch.object(DatabaseUser, "drop", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_user_drop_item_fulfill_not_drop(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserDropItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=False))
    mocker.patch.object(DatabaseUser, "_get_password", return_value="example")

    spy_drop = mocker.spy(object_.database_user, "drop")

    object_.fulfill()

    spy_drop.assert_not_called()

from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant

from cyberfusion.QueueSupport.items.database_user_grant_grant import (
    DatabaseUserGrantGrantItem,
)
from pytest_mock import MockerFixture


MODE = 0o755


def test_database_user_grant_grant_item_fulfill_grant(mocker: MockerFixture) -> None:
    object_ = DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="test",
        database_user_name="test",
        privilege_names=["ALL"],
        table=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=False)
    )
    mock = mocker.patch.object(DatabaseUserGrant, "grant", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_user_grant_grant_item_fulfill_not_grant(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserGrantGrantItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="test",
        database_user_name="test",
        privilege_names=["ALL"],
        table=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=True)
    )

    spy_grant = mocker.spy(object_.database_user_grant, "grant")

    object_.fulfill()

    spy_grant.assert_not_called()

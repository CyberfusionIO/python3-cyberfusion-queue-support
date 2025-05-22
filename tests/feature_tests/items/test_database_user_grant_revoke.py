from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant

from cyberfusion.QueueSupport.items.database_user_grant_revoke import (
    DatabaseUserGrantRevokeItem,
)
from pytest_mock import MockerFixture


MODE = 0o755


def test_database_user_grant_revoke_item_fulfill_revoke(mocker: MockerFixture) -> None:
    object_ = DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="test",
        database_user_name="test",
        privilege_names=["ALL"],
        table=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=True)
    )
    mock = mocker.patch.object(DatabaseUserGrant, "revoke", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_user_grant_revoke_item_fulfill_not_revoke(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserGrantRevokeItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        database_name="test",
        database_user_name="test",
        privilege_names=["ALL"],
        table=None,
    )

    mocker.patch.object(
        DatabaseUserGrant, "exists", new=PropertyMock(return_value=False)
    )

    spy_revoke = mocker.spy(object_.database_user_grant, "revoke")

    object_.fulfill()

    spy_revoke.assert_not_called()

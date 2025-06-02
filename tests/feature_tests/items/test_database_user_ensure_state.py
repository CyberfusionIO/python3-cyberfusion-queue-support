from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_users import DatabaseUser

from cyberfusion.QueueSupport.items.database_user_ensure_state import (
    DatabaseUserEnsureStateItem,
)
from pytest_mock import MockerFixture


MODE = 0o755


def test_database_user_ensure_state_item_fulfill_create(mocker: MockerFixture) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=False))
    mock = mocker.patch.object(DatabaseUser, "create", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_user_ensure_state_item_fulfill_edit_password(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=True))
    mocker.patch.object(DatabaseUser, "_get_password", return_value="password")
    mock = mocker.patch.object(DatabaseUser, "edit", return_value=True)

    object_.fulfill()

    mock.assert_called_once()


def test_database_user_ensure_state_item_fulfill_not_create(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=True))
    mocker.patch.object(DatabaseUser, "_get_password", return_value="example")

    spy_create = mocker.spy(object_.database_user, "create")

    object_.fulfill()

    spy_create.assert_not_called()


def test_database_user_ensure_state_item_fulfill_not_edit_password(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=True))
    mocker.patch.object(DatabaseUser, "_get_password", return_value="example")

    spy_edit = mocker.spy(object_.database_user, "edit")

    object_.fulfill()

    spy_edit.assert_not_called()

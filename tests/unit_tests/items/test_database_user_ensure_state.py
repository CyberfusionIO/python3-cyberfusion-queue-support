from unittest.mock import PropertyMock

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_users import DatabaseUser
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.items.database_user_ensure_state import (
    DatabaseUserEnsureStateItem,
)
from cyberfusion.QueueSupport.outcomes import DatabaseUserEnsureStateItemCreateOutcome

MODE = 0o755

# Equal


def test_database_user_ensure_state_item_equal() -> None:
    assert DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    ) == DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    )


def test_database_user_create_item_not_equal_server_software_name() -> None:
    assert DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    ) != DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    )


def test_database_user_ensure_state_item_not_equal_name() -> None:
    assert DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    ) != DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="test",
        password="example",
    )


def test_database_user_ensure_state_item_not_equal_password() -> None:
    assert DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    ) != DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="test",
    )


def test_database_user_ensure_state_item_not_equal_host() -> None:
    assert DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
        host="example",
    ) != DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="test",
        host="test",
    )


def test_database_user_ensure_state_item_not_equal_different_type() -> None:
    assert (
        DatabaseUserEnsureStateItem(
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="example",
            password="example",
        )
        == 5
    ) is False


# Outcomes


def test_database_user_ensure_state_item_not_exists_has_outcome_create(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=False))

    assert object_.outcomes == [
        DatabaseUserEnsureStateItemCreateOutcome(database_user=object_.database_user)
    ]


def test_database_user_ensure_state_item_exists_different_password_has_outcome_create(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=False))
    mocker.patch.object(object_.database_user, "_get_password", return_value="test")

    assert object_.outcomes == [
        DatabaseUserEnsureStateItemCreateOutcome(database_user=object_.database_user)
    ]


def test_database_user_ensure_state_item_exists_same_password_not_has_outcome_create(
    mocker: MockerFixture,
) -> None:
    object_ = DatabaseUserEnsureStateItem(
        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        name="example",
        password="example",
    )

    mocker.patch.object(DatabaseUser, "exists", new=PropertyMock(return_value=True))
    mocker.patch.object(object_.database_user, "_get_password", return_value="example")

    print(object_.database_user.password)
    print(object_.database_user._get_password())

    assert object_.outcomes == []

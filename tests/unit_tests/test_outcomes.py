from typing import Generator


from cyberfusion.Common import generate_random_string
from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.database_user_grants import DatabaseUserGrant
from cyberfusion.DatabaseSupport.database_users import DatabaseUser
from cyberfusion.DatabaseSupport.databases import Database
from cyberfusion.DatabaseSupport.servers import Server
from sqlalchemy import Table, MetaData

from cyberfusion.QueueSupport.outcomes import (
    ChmodItemModeChangeOutcome,
    ChownItemGroupChangeOutcome,
    ChownItemOwnerChangeOutcome,
    CommandItemRunOutcome,
    CopyItemCopyOutcome,
    MkdirItemCreateOutcome,
    MoveItemMoveOutcome,
    SystemdTmpFilesCreateItemCreateOutcome,
    SystemdUnitDisableItemDisableOutcome,
    SystemdUnitEnableItemEnableOutcome,
    SystemdUnitStartItemStartOutcome,
    SystemdDaemonReloadItemReloadOutcome,
    SystemdUnitReloadItemReloadOutcome,
    SystemdUnitRestartItemRestartOutcome,
    SystemdUnitStopItemStopOutcome,
    UnlinkItemUnlinkOutcome,
    RmTreeItemRemoveOutcome,
    DatabaseCreateItemCreateOutcome,
    DatabaseUserEnsureStateItemCreateOutcome,
    DatabaseUserEnsureStateItemEditPasswordOutcome,
    DatabaseUserGrantGrantItemGrantOutcome,
    DatabaseDropItemDropOutcome,
    DatabaseUserDropItemDropOutcome,
    DatabaseUserGrantRevokeItemRevokeOutcome,
)
from cyberfusion.SystemdSupport.units import Unit

MODE = 0o644

# String


def test_chmod_item_mode_change_outcome_string_with_old_mode(
    non_existent_path: str,
) -> None:
    assert (
        str(
            ChmodItemModeChangeOutcome(
                path=non_existent_path, old_mode=0o600, new_mode=0o644
            )
        )
        == f"Change mode of {non_existent_path} from 0o600 to 0o644"
    )


def test_chmod_item_mode_change_outcome_string_without_old_mode(
    non_existent_path: str,
) -> None:
    assert (
        str(
            ChmodItemModeChangeOutcome(
                path=non_existent_path, old_mode=None, new_mode=0o644
            )
        )
        == f"Change mode of {non_existent_path} from None to 0o644"
    )


def test_mkdir_item_create_outcome_string(non_existent_path: str) -> None:
    assert (
        str(
            MkdirItemCreateOutcome(
                path=non_existent_path,
            )
        )
        == f"Create {non_existent_path}"
    )


def test_copy_item_copy_outcome_string(
    non_existent_path: str, existent_file_path: Generator[str, None, None]
) -> None:
    assert (
        str(
            CopyItemCopyOutcome(
                source=non_existent_path,
                destination=existent_file_path,
            )
        )
        == f"Copy {non_existent_path} to {existent_file_path}."
    )


def test_copy_item_copy_changed_lines_outcome_string(
    non_existent_path: str, existent_file_path: Generator[str, None, None]
) -> None:
    changed_lines = ["example", "example2"]
    changed_lines_string = "\n".join(changed_lines)

    assert (
        str(
            CopyItemCopyOutcome(
                source=non_existent_path,
                destination=existent_file_path,
                changed_lines=changed_lines,
            )
        )
        == f"Copy {non_existent_path} to {existent_file_path}.\nChanged lines:\n{changed_lines_string}"
    )


def test_move_item_move_outcome_string(
    non_existent_path: str, existent_file_path: Generator[str, None, None]
) -> None:
    assert (
        str(
            MoveItemMoveOutcome(
                source=non_existent_path,
                destination=existent_file_path,
            )
        )
        == f"Move {non_existent_path} to {existent_file_path}"
    )


def test_rmtree_item_remove_outcome_string(non_existent_path: str) -> None:
    assert (
        str(
            RmTreeItemRemoveOutcome(
                path=non_existent_path,
            )
        )
        == f"Remove directory tree {non_existent_path}"
    )


def test_unlink_item_unlink_outcome_string(non_existent_path: str) -> None:
    assert (
        str(
            UnlinkItemUnlinkOutcome(
                path=non_existent_path,
            )
        )
        == f"Unlink {non_existent_path}"
    )


def test_command_item_run_outcome_string(non_existent_path: str) -> None:
    assert str(CommandItemRunOutcome(command="true")) == "Run true"


def test_chmod_item_owner_name_change_outcome_string(
    non_existent_path: str,
) -> None:
    assert (
        str(
            ChownItemOwnerChangeOutcome(
                path=non_existent_path,
                old_owner_name="old",
                new_owner_name="new",
            )
        )
        == f"Change owner of {non_existent_path} from old to new"
    )


def test_chmod_item_group_name_change_outcome_string(
    non_existent_path: str,
) -> None:
    assert (
        str(
            ChownItemGroupChangeOutcome(
                path=non_existent_path,
                old_group_name="old",
                new_group_name="new",
            )
        )
        == f"Change group of {non_existent_path} from old to new"
    )


def test_systemd_unit_enable_item_enable_outcome_string() -> None:
    assert (
        str(SystemdUnitEnableItemEnableOutcome(unit=Unit("example")))
        == "Enable example"
    )


def test_systemd_unit_start_item_start_outcome_string() -> None:
    assert (
        str(SystemdUnitStartItemStartOutcome(unit=Unit("example"))) == "Start example"
    )


def test_systemd_daemon_reload_item_reload_outcome_string() -> None:
    assert str(SystemdDaemonReloadItemReloadOutcome()) == "Reload daemon"


def test_systemd_unit_stop_item_stop_outcome_string() -> None:
    assert str(SystemdUnitStopItemStopOutcome(unit=Unit("example"))) == "Stop example"


def test_systemd_unit_disable_item_disable_outcome_string() -> None:
    assert (
        str(SystemdUnitDisableItemDisableOutcome(unit=Unit("example")))
        == "Disable example"
    )


def test_systemd_unit_restart_item_restart_outcome_string() -> None:
    assert (
        str(SystemdUnitRestartItemRestartOutcome(unit=Unit("example")))
        == "Restart example"
    )


def test_systemd_unit_reload_item_reload_outcome_string() -> None:
    assert (
        str(SystemdUnitReloadItemReloadOutcome(unit=Unit("example")))
        == "Reload example"
    )


def test_systemd_tmp_files_create_item_create_outcome_string() -> None:
    assert (
        str(SystemdTmpFilesCreateItemCreateOutcome(path="/tmp/example"))
        == "Create tmp files according to tmp files configuration file at /tmp/example"
    )


def test_database_create_item_create_outcome_string() -> None:
    assert (
        str(
            DatabaseCreateItemCreateOutcome(
                database=Database(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    ),
                    name="test",
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                )
            )
        )
        == "Create test in MariaDB"
    )


def test_database_drop_item_drop_outcome_string() -> None:
    assert (
        str(
            DatabaseDropItemDropOutcome(
                database=Database(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    ),
                    name="test",
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                )
            )
        )
        == "Drop test in MariaDB"
    )


def test_database_user_ensure_state_item_create_outcome_string() -> None:
    assert (
        str(
            DatabaseUserEnsureStateItemCreateOutcome(
                database_user=DatabaseUser(
                    server=Server(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        )
                    ),
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    name="test",
                )
            )
        )
        == "Create test in MariaDB"
    )


def test_database_user_ensure_state_item_edit_password_outcome_string() -> None:
    assert (
        str(
            DatabaseUserEnsureStateItemEditPasswordOutcome(
                database_user=DatabaseUser(
                    server=Server(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        )
                    ),
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    name="test",
                )
            )
        )
        == "Edit password of test in MariaDB"
    )


def test_database_user_drop_item_drop_outcome_string() -> None:
    assert (
        str(
            DatabaseUserDropItemDropOutcome(
                database_user=DatabaseUser(
                    server=Server(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        )
                    ),
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    name="test",
                )
            )
        )
        == "Drop test in MariaDB"
    )


def test_database_user_grant_grant_item_create_outcome_string() -> None:
    assert (
        str(
            DatabaseUserGrantGrantItemGrantOutcome(
                database_user_grant=DatabaseUserGrant(
                    database=Database(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        ),
                        name="test",
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    ),
                    database_user=DatabaseUser(
                        server=Server(
                            support=DatabaseSupport(
                                server_software_names=[
                                    DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                                ]
                            )
                        ),
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                        name="test",
                    ),
                    privilege_names=["ALL"],
                    table=None,
                )
            )
        )
        == "Grant ['ALL'] to * in test in MariaDB"
    )


def test_database_user_grant_grant_item_create_outcome_string_table_name() -> None:
    assert (
        str(
            DatabaseUserGrantGrantItemGrantOutcome(
                database_user_grant=DatabaseUserGrant(
                    database=Database(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        ),
                        name="test",
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    ),
                    database_user=DatabaseUser(
                        server=Server(
                            support=DatabaseSupport(
                                server_software_names=[
                                    DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                                ]
                            )
                        ),
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                        name="test",
                    ),
                    privilege_names=["ALL"],
                    table=Table("example", MetaData()),
                )
            )
        )
        == "Grant ['ALL'] to example in test in MariaDB"
    )


def test_database_user_grant_revoke_item_revoke_outcome_string() -> None:
    assert (
        str(
            DatabaseUserGrantRevokeItemRevokeOutcome(
                database_user_grant=DatabaseUserGrant(
                    database=Database(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        ),
                        name="test",
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    ),
                    database_user=DatabaseUser(
                        server=Server(
                            support=DatabaseSupport(
                                server_software_names=[
                                    DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                                ]
                            )
                        ),
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                        name="test",
                    ),
                    privilege_names=["ALL"],
                    table=None,
                )
            )
        )
        == "Revoke ['ALL'] to * in test in MariaDB"
    )


def test_database_user_grant_revoke_item_revoke_outcome_string_table_name() -> None:
    assert (
        str(
            DatabaseUserGrantRevokeItemRevokeOutcome(
                database_user_grant=DatabaseUserGrant(
                    database=Database(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        ),
                        name="test",
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    ),
                    database_user=DatabaseUser(
                        server=Server(
                            support=DatabaseSupport(
                                server_software_names=[
                                    DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                                ]
                            )
                        ),
                        server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                        name="test",
                    ),
                    privilege_names=["ALL"],
                    table=Table("example", MetaData()),
                )
            )
        )
        == "Revoke ['ALL'] to example in test in MariaDB"
    )


# Equal: ChmodItemModeChangeOutcome


def test_chmod_item_mode_change_outcome_equal(non_existent_path: str) -> None:
    assert ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE, new_mode=MODE
    ) == ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE, new_mode=MODE
    )


def test_chmod_item_mode_change_outcome_not_equal_path(
    non_existent_path: str,
) -> None:
    assert ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE, new_mode=MODE
    ) != ChmodItemModeChangeOutcome(
        path=non_existent_path + "-example", old_mode=MODE, new_mode=MODE
    )


def test_chmod_item_mode_change_outcome_not_equal_old_mode(
    non_existent_path: str,
) -> None:
    assert ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE, new_mode=MODE
    ) != ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE + 1, new_mode=MODE
    )


def test_chmod_item_mode_change_outcome_not_equal_new_mode(
    non_existent_path: str,
) -> None:
    assert ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE, new_mode=MODE
    ) != ChmodItemModeChangeOutcome(
        path=non_existent_path, old_mode=MODE, new_mode=MODE + 1
    )


def test_chmod_item_mode_change_outcome_equal_different_type(
    non_existent_path: str,
) -> None:
    assert (
        ChmodItemModeChangeOutcome(path=non_existent_path, old_mode=MODE, new_mode=MODE)
        == 5
    ) is False


# Equal: MkdirItemCreateOutcome


def test_mkdir_item_create_outcome_equal(non_existent_path: str) -> None:
    assert MkdirItemCreateOutcome(
        path=non_existent_path,
    ) == MkdirItemCreateOutcome(
        path=non_existent_path,
    )


def test_mkdir_item_create_outcome_not_equal_path(
    non_existent_path: str,
) -> None:
    assert MkdirItemCreateOutcome(
        path=non_existent_path,
    ) != MkdirItemCreateOutcome(
        path=non_existent_path + "-example",
    )


def test_mkdir_item_create_outcome_equal_different_type(
    non_existent_path: str,
) -> None:
    assert (
        MkdirItemCreateOutcome(
            path=non_existent_path,
        )
        == 5
    ) is False


# Equal: CopyItemCopyOutcome


def test_copy_item_copy_outcome_equal(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path, changed_lines=[]
    ) == CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path, changed_lines=[]
    )


def test_copy_item_copy_outcome_not_equal_source(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path, changed_lines=[]
    ) != CopyItemCopyOutcome(
        source=existent_file_path + "-example",
        destination=non_existent_path,
        changed_lines=[],
    )


def test_copy_item_copy_outcome_not_equal_destination(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path, changed_lines=[]
    ) != CopyItemCopyOutcome(
        source=existent_file_path,
        destination=non_existent_path + "-example",
        changed_lines=[],
    )


def test_copy_item_copy_outcome_not_equal_changed_lines(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path, changed_lines=[]
    ) != CopyItemCopyOutcome(
        source=existent_file_path,
        destination=non_existent_path,
        changed_lines=["example"],
    )


def test_copy_item_copy_outcome_equal_different_type(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert (
        CopyItemCopyOutcome(
            source=existent_file_path, destination=non_existent_path, changed_lines=[]
        )
        == 5
    ) is False


# Equal: MoveItemMoveOutcome


def test_move_item_move_outcome_equal(
    existent_file_path: Generator[str, None, None], non_existent_path: str
) -> None:
    assert MoveItemMoveOutcome(
        source=existent_file_path, destination=non_existent_path
    ) == MoveItemMoveOutcome(source=existent_file_path, destination=non_existent_path)


def test_move_item_move_outcome_not_equal_source(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert MoveItemMoveOutcome(
        source=existent_file_path, destination=non_existent_path
    ) != MoveItemMoveOutcome(
        source=existent_file_path + "-example", destination=non_existent_path
    )


def test_move_item_move_outcome_not_equal_destination(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert MoveItemMoveOutcome(
        source=existent_file_path, destination=non_existent_path
    ) != MoveItemMoveOutcome(
        source=existent_file_path, destination=non_existent_path + "-example"
    )


def test_move_item_move_outcome_equal_different_type(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert (
        MoveItemMoveOutcome(source=existent_file_path, destination=non_existent_path)
        == 5
    ) is False


# Equal: RmTreeItemRemoveOutcome


def test_rmtree_item_remove_outcome_equal(non_existent_path: str) -> None:
    assert RmTreeItemRemoveOutcome(
        path=non_existent_path,
    ) == RmTreeItemRemoveOutcome(
        path=non_existent_path,
    )


def test_rmtree_item_remove_outcome_not_equal_path(
    non_existent_path: str,
) -> None:
    assert RmTreeItemRemoveOutcome(
        path=non_existent_path,
    ) != RmTreeItemRemoveOutcome(
        path=non_existent_path + "-example",
    )


def test_rmtree_item_remove_outcome_equal_different_type(
    non_existent_path: str,
) -> None:
    assert (
        RmTreeItemRemoveOutcome(
            path=non_existent_path,
        )
        == 5
    ) is False


# Equal: UnlinkItemUnlinkOutcome


def test_unlink_item_unlink_outcome_equal(non_existent_path: str) -> None:
    assert UnlinkItemUnlinkOutcome(
        path=non_existent_path,
    ) == UnlinkItemUnlinkOutcome(
        path=non_existent_path,
    )


def test_unlink_item_unlink_outcome_not_equal_path(
    non_existent_path: str,
) -> None:
    assert UnlinkItemUnlinkOutcome(
        path=non_existent_path,
    ) != UnlinkItemUnlinkOutcome(
        path=non_existent_path + "-example",
    )


def test_unlink_item_unlink_outcome_equal_different_type(
    non_existent_path: str,
) -> None:
    assert (
        UnlinkItemUnlinkOutcome(
            path=non_existent_path,
        )
        == 5
    ) is False


# Equal: CommandItemRunOutcome


def test_command_item_run_outcome_equal() -> None:
    assert CommandItemRunOutcome(
        command="true",
    ) == CommandItemRunOutcome(command="true")


def test_command_item_run_outcome_not_equal_command() -> None:
    assert CommandItemRunOutcome(
        command="true", stdout="example", stderr="example"
    ) != CommandItemRunOutcome(command="false", stdout="example", stderr="example")


def test_command_item_run_outcome_not_equal_stdout() -> None:
    assert CommandItemRunOutcome(
        command="true", stdout="example" + generate_random_string(), stderr="example"
    ) != CommandItemRunOutcome(
        command="true", stdout="example" + generate_random_string(), stderr="example"
    )


def test_command_item_run_outcome_not_equal_stderr() -> None:
    assert CommandItemRunOutcome(
        command="true", stdout="example", stderr="example" + generate_random_string()
    ) != CommandItemRunOutcome(
        command="true", stdout="example", stderr="example" + generate_random_string()
    )


def test_command_item_run_outcome_equal_different_type() -> None:
    assert (
        CommandItemRunOutcome(
            command="true",
        )
        == 5
    ) is False


# Equal: ChownItemOwnerChangeOutcome


def test_chmod_item_owner_name_change_outcome_equal(
    non_existent_path: str,
) -> None:
    assert ChownItemOwnerChangeOutcome(
        path=non_existent_path, old_owner_name="old", new_owner_name="new"
    ) == ChownItemOwnerChangeOutcome(
        path=non_existent_path, old_owner_name="old", new_owner_name="new"
    )


def test_chmod_item_owner_name_change_outcome_not_equal_path(
    non_existent_path: str,
) -> None:
    assert ChownItemOwnerChangeOutcome(
        path=non_existent_path, old_owner_name="old", new_owner_name="new"
    ) != ChownItemOwnerChangeOutcome(
        path=non_existent_path + "-example",
        old_owner_name="old",
        new_owner_name="new",
    )


def test_chmod_item_owner_name_change_outcome_not_equal_old_owner_name(
    non_existent_path: str,
) -> None:
    assert ChownItemOwnerChangeOutcome(
        path=non_existent_path, old_owner_name="old", new_owner_name="new"
    ) != ChownItemOwnerChangeOutcome(
        path=non_existent_path,
        old_owner_name="old" + generate_random_string(),
        new_owner_name="new",
    )


def test_chmod_item_owner_name_change_outcome_not_equal_new_owner_name(
    non_existent_path: str,
) -> None:
    assert ChownItemOwnerChangeOutcome(
        path=non_existent_path, old_owner_name="old", new_owner_name="new"
    ) != ChownItemOwnerChangeOutcome(
        path=non_existent_path,
        old_owner_name="old",
        new_owner_name="new" + generate_random_string(),
    )


def test_chmod_item_owner_name_change_outcome_equal_different_type(
    non_existent_path: str,
) -> None:
    assert (
        ChownItemOwnerChangeOutcome(
            path=non_existent_path, old_owner_name="old", new_owner_name="new"
        )
        == 5
    ) is False


# Equal: ChownItemGroupChangeOutcome


def test_chmod_item_group_name_change_outcome_equal(
    non_existent_path: str,
) -> None:
    assert ChownItemGroupChangeOutcome(
        path=non_existent_path, old_group_name="old", new_group_name="new"
    ) == ChownItemGroupChangeOutcome(
        path=non_existent_path, old_group_name="old", new_group_name="new"
    )


def test_chmod_item_group_name_change_outcome_not_equal_path(
    non_existent_path: str,
) -> None:
    assert ChownItemGroupChangeOutcome(
        path=non_existent_path, old_group_name="old", new_group_name="new"
    ) != ChownItemGroupChangeOutcome(
        path=non_existent_path + "-example",
        old_group_name="old",
        new_group_name="new",
    )


def test_chmod_item_group_name_change_outcome_not_equal_old_group_name(
    non_existent_path: str,
) -> None:
    assert ChownItemGroupChangeOutcome(
        path=non_existent_path, old_group_name="old", new_group_name="new"
    ) != ChownItemGroupChangeOutcome(
        path=non_existent_path,
        old_group_name="old" + generate_random_string(),
        new_group_name="new",
    )


def test_chmod_item_group_name_change_outcome_not_equal_new_group_name(
    non_existent_path: str,
) -> None:
    assert ChownItemGroupChangeOutcome(
        path=non_existent_path, old_group_name="old", new_group_name="new"
    ) != ChownItemGroupChangeOutcome(
        path=non_existent_path,
        old_group_name="old",
        new_group_name="new" + generate_random_string(),
    )


def test_chmod_item_group_name_change_outcome_equal_different_type(
    non_existent_path: str,
) -> None:
    assert (
        ChownItemGroupChangeOutcome(
            path=non_existent_path, old_group_name="old", new_group_name="new"
        )
        == 5
    ) is False


# Equal: SystemdUnitEnableItemEnableOutcome


def test_systemd_unit_enable_item_enable_outcome_equal() -> None:
    assert SystemdUnitEnableItemEnableOutcome(
        unit=Unit("example")
    ) == SystemdUnitEnableItemEnableOutcome(unit=Unit("example"))


def test_systemd_unit_enable_item_enable_outcome_not_equal_unit() -> None:
    assert SystemdUnitEnableItemEnableOutcome(
        unit=Unit("example"),
    ) != SystemdUnitEnableItemEnableOutcome(unit=Unit("example-example"))


def test_systemd_unit_enable_item_enable_outcome_equal_different_type() -> None:
    assert (SystemdUnitEnableItemEnableOutcome(unit=Unit("example")) == 5) is False


# Equal: SystemdUnitStartItemStartOutcome


def test_systemd_unit_start_item_start_outcome_equal() -> None:
    assert SystemdUnitStartItemStartOutcome(
        unit=Unit("example")
    ) == SystemdUnitStartItemStartOutcome(unit=Unit("example"))


def test_systemd_unit_start_item_start_outcome_not_equal_unit() -> None:
    assert SystemdUnitStartItemStartOutcome(
        unit=Unit("example"),
    ) != SystemdUnitStartItemStartOutcome(unit=Unit("example-example"))


def test_systemd_unit_start_item_start_outcome_equal_different_type() -> None:
    assert (SystemdUnitStartItemStartOutcome(unit=Unit("example")) == 5) is False


# Equal: SystemdUnitReloadItemReloadOutcome


def test_systemd_daemon_reload_item_reload_outcome_equal() -> None:
    assert (
        SystemdDaemonReloadItemReloadOutcome() == SystemdDaemonReloadItemReloadOutcome()
    )


def test_systemd_daemon_reload_item_reload_outcome_equal_different_type() -> None:
    assert (SystemdDaemonReloadItemReloadOutcome() == 5) is False


# Equal: SystemdUnitStopItemStopOutcome


def test_systemd_unit_stop_item_stop_outcome_equal() -> None:
    assert SystemdUnitStopItemStopOutcome(
        unit=Unit("example")
    ) == SystemdUnitStopItemStopOutcome(unit=Unit("example"))


def test_systemd_unit_stop_item_stop_outcome_not_equal_unit() -> None:
    assert SystemdUnitStopItemStopOutcome(
        unit=Unit("example"),
    ) != SystemdUnitStopItemStopOutcome(unit=Unit("example-example"))


def test_systemd_unit_stop_item_stop_outcome_equal_different_type() -> None:
    assert (SystemdUnitStopItemStopOutcome(unit=Unit("example")) == 5) is False


# Equal: SystemdUnitDisableItemDisableOutcome


def test_systemd_unit_disable_item_disable_outcome_equal() -> None:
    assert SystemdUnitDisableItemDisableOutcome(
        unit=Unit("example")
    ) == SystemdUnitDisableItemDisableOutcome(unit=Unit("example"))


def test_systemd_unit_disable_item_disable_outcome_not_equal_unit() -> None:
    assert SystemdUnitDisableItemDisableOutcome(
        unit=Unit("example"),
    ) != SystemdUnitDisableItemDisableOutcome(unit=Unit("example-example"))


def test_systemd_unit_disable_item_disable_outcome_equal_different_type() -> None:
    assert (SystemdUnitDisableItemDisableOutcome(unit=Unit("example")) == 5) is False


# Equal: SystemdUnitRestartItemRestartOutcome


def test_systemd_unit_restart_item_restart_outcome_equal() -> None:
    assert SystemdUnitRestartItemRestartOutcome(
        unit=Unit("example")
    ) == SystemdUnitRestartItemRestartOutcome(unit=Unit("example"))


def test_systemd_unit_restart_item_restart_outcome_not_equal_unit() -> None:
    assert SystemdUnitRestartItemRestartOutcome(
        unit=Unit("example"),
    ) != SystemdUnitRestartItemRestartOutcome(unit=Unit("example-example"))


def test_systemd_unit_restart_item_restart_outcome_equal_different_type() -> None:
    assert (SystemdUnitRestartItemRestartOutcome(unit=Unit("example")) == 5) is False


# Equal: SystemdUnitReloadItemReloadOutcome


def test_systemd_unit_reload_item_reload_outcome_equal() -> None:
    assert SystemdUnitReloadItemReloadOutcome(
        unit=Unit("example")
    ) == SystemdUnitReloadItemReloadOutcome(unit=Unit("example"))


def test_systemd_unit_reload_item_reload_outcome_not_equal_unit() -> None:
    assert SystemdUnitReloadItemReloadOutcome(
        unit=Unit("example"),
    ) != SystemdUnitReloadItemReloadOutcome(unit=Unit("example-example"))


def test_systemd_unit_reload_item_reload_outcome_equal_different_type() -> None:
    assert (SystemdUnitReloadItemReloadOutcome(unit=Unit("example")) == 5) is False


# Equal: SystemdTmpFilesCreateItemCreateOutcome


def test_systemd_tmp_files_create_item_create_outcome_equal() -> None:
    assert SystemdTmpFilesCreateItemCreateOutcome(
        path="/tmp/example"
    ) == SystemdTmpFilesCreateItemCreateOutcome(path="/tmp/example")


def test_systemd_tmp_files_create_item_create_outcome_not_equal_unit() -> None:
    assert SystemdTmpFilesCreateItemCreateOutcome(
        path="/tmp/example",
    ) != SystemdTmpFilesCreateItemCreateOutcome(path="/tmp/example/example")


def test_systemd_tmp_files_create_item_create_outcome_equal_different_type() -> None:
    assert (SystemdTmpFilesCreateItemCreateOutcome(path="/tmp/example") == 5) is False


# Equal: DatabaseCreateItemCreateOutcome


def test_database_create_item_create_outcome_equal() -> None:
    assert DatabaseCreateItemCreateOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
            ),
            name="test",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    ) == DatabaseCreateItemCreateOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
            ),
            name="test",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    )


def test_database_create_item_create_outcome_not_equal_different_database() -> None:
    assert DatabaseCreateItemCreateOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
            ),
            name="test",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    ) != DatabaseCreateItemCreateOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME]
            ),
            name="example",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    )


def test_database_create_item_create_outcome_not_equal_different_type() -> None:
    assert (
        DatabaseCreateItemCreateOutcome(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            )
        )
        == 5
    ) is False


# Equal: DatabaseDropItemDropOutcome


def test_database_drop_item_drop_outcome_equal() -> None:
    assert DatabaseDropItemDropOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
            ),
            name="test",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    ) == DatabaseDropItemDropOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
            ),
            name="test",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    )


def test_database_drop_item_drop_outcome_not_equal_different_database() -> None:
    assert DatabaseDropItemDropOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
            ),
            name="test",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    ) != DatabaseDropItemDropOutcome(
        database=Database(
            support=DatabaseSupport(
                server_software_names=[DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME]
            ),
            name="example",
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )
    )


def test_database_drop_item_drop_outcome_not_equal_different_type() -> None:
    assert (
        DatabaseDropItemDropOutcome(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            )
        )
        == 5
    ) is False


# Equal: DatabaseUserEnsureStateItemCreateOutcome


def test_database_user_ensure_state_item_create_outcome_equal() -> None:
    assert DatabaseUserEnsureStateItemCreateOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    ) == DatabaseUserEnsureStateItemCreateOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    )


def test_database_user_ensure_state_item_create_outcome_not_equal_different_database_user() -> (
    None
):
    assert DatabaseUserEnsureStateItemCreateOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    ) != DatabaseUserEnsureStateItemCreateOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[
                        DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME
                    ]
                )
            ),
            server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
            name="example",
        )
    )


def test_database_user_ensure_state_item_create_outcome_not_equal_different_type() -> (
    None
):
    assert (
        DatabaseUserEnsureStateItemCreateOutcome(
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            )
        )
        == 5
    ) is False


# Equal: DatabaseUserEnsureStateItemEditPasswordOutcome


def test_database_user_ensure_state_item_edit_password_outcome_equal() -> None:
    assert DatabaseUserEnsureStateItemEditPasswordOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    ) == DatabaseUserEnsureStateItemEditPasswordOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    )


def test_database_user_ensure_state_item_edit_password_outcome_not_equal_different_database_user() -> (
    None
):
    assert DatabaseUserEnsureStateItemEditPasswordOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    ) != DatabaseUserEnsureStateItemEditPasswordOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[
                        DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME
                    ]
                )
            ),
            server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
            name="example",
        )
    )


def test_database_user_ensure_state_item_edit_password_outcome_not_equal_different_type() -> (
    None
):
    assert (
        DatabaseUserEnsureStateItemEditPasswordOutcome(
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            )
        )
        == 5
    ) is False


# Equal: DatabaseUserDropItemDropOutcome


def test_database_user_drop_item_drop_outcome_equal() -> None:
    assert DatabaseUserDropItemDropOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    ) == DatabaseUserDropItemDropOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    )


def test_database_user_drop_item_drop_outcome_not_equal_different_database_user() -> (
    None
):
    assert DatabaseUserDropItemDropOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                )
            ),
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            name="test",
        )
    ) != DatabaseUserDropItemDropOutcome(
        database_user=DatabaseUser(
            server=Server(
                support=DatabaseSupport(
                    server_software_names=[
                        DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME
                    ]
                )
            ),
            server_software_name=DatabaseSupport.POSTGRESQL_SERVER_SOFTWARE_NAME,
            name="example",
        )
    )


def test_database_user_drop_item_drop_outcome_not_equal_different_type() -> None:
    assert (
        DatabaseUserDropItemDropOutcome(
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            )
        )
        == 5
    ) is False


# Equal: DatabaseUserGrantGrantItemGrantOutcome


def test_database_user_grant_grant_item_grant_outcome_equal() -> None:
    assert DatabaseUserGrantGrantItemGrantOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            ),
            privilege_names=["ALL"],
            table=None,
        )
    ) == DatabaseUserGrantGrantItemGrantOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            ),
            privilege_names=["ALL"],
            table=None,
        )
    )


def test_database_user_grant_grant_item_grant_outcome_not_equal_different_database_user_grant() -> (
    None
):
    assert DatabaseUserGrantGrantItemGrantOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            ),
            privilege_names=["ALL"],
            table=None,
        )
    ) != DatabaseUserGrantGrantItemGrantOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="example",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="example",
            ),
            privilege_names=["SELECT"],
            table=Table("example", MetaData()),
        )
    )


def test_database_user_grant_grant_item_grant_outcome_not_equal_different_type() -> (
    None
):
    assert (
        DatabaseUserGrantGrantItemGrantOutcome(
            database_user_grant=DatabaseUserGrant(
                database=Database(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    ),
                    name="test",
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                ),
                database_user=DatabaseUser(
                    server=Server(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        )
                    ),
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    name="test",
                ),
                privilege_names=["ALL"],
                table=None,
            )
        )
        == 5
    ) is False


# Equal: DatabaseUserGrantRevokeItemRevokeOutcome


def test_database_user_grant_revoke_item_revoke_outcome_equal() -> None:
    assert DatabaseUserGrantRevokeItemRevokeOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            ),
            privilege_names=["ALL"],
            table=None,
        )
    ) == DatabaseUserGrantRevokeItemRevokeOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            ),
            privilege_names=["ALL"],
            table=None,
        )
    )


def test_database_user_grant_revoke_item_revoke_outcome_not_equal_different_database_user_grant() -> (
    None
):
    assert DatabaseUserGrantRevokeItemRevokeOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="test",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="test",
            ),
            privilege_names=["ALL"],
            table=None,
        )
    ) != DatabaseUserGrantRevokeItemRevokeOutcome(
        database_user_grant=DatabaseUserGrant(
            database=Database(
                support=DatabaseSupport(
                    server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME]
                ),
                name="example",
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
            ),
            database_user=DatabaseUser(
                server=Server(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    )
                ),
                server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                name="example",
            ),
            privilege_names=["SELECT"],
            table=Table("example", MetaData()),
        )
    )


def test_database_user_grant_revoke_item_revoke_outcome_not_equal_different_type() -> (
    None
):
    assert (
        DatabaseUserGrantRevokeItemRevokeOutcome(
            database_user_grant=DatabaseUserGrant(
                database=Database(
                    support=DatabaseSupport(
                        server_software_names=[
                            DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                        ]
                    ),
                    name="test",
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                ),
                database_user=DatabaseUser(
                    server=Server(
                        support=DatabaseSupport(
                            server_software_names=[
                                DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
                            ]
                        )
                    ),
                    server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
                    name="test",
                ),
                privilege_names=["ALL"],
                table=None,
            )
        )
        == 5
    ) is False

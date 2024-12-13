from typing import Generator


from cyberfusion.Common import generate_random_string
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
    SystemdUnitReloadItemReloadOutcome,
    SystemdUnitRestartItemRestartOutcome,
    SystemdUnitStopItemStopOutcome,
    UnlinkItemUnlinkOutcome,
    RmTreeItemRemoveOutcome,
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


def test_copy_item_create_outcome_string(
    non_existent_path: str, existent_file_path: Generator[str, None, None]
) -> None:
    assert (
        str(
            CopyItemCopyOutcome(
                source=non_existent_path,
                destination=existent_file_path,
            )
        )
        == f"Copy {non_existent_path} to {existent_file_path}"
    )


def test_move_item_create_outcome_string(
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
        source=existent_file_path, destination=non_existent_path
    ) == CopyItemCopyOutcome(source=existent_file_path, destination=non_existent_path)


def test_copy_item_copy_outcome_not_equal_source(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path
    ) != CopyItemCopyOutcome(
        source=existent_file_path + "-example", destination=non_existent_path
    )


def test_copy_item_copy_outcome_not_equal_destination(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path
    ) != CopyItemCopyOutcome(
        source=existent_file_path, destination=non_existent_path + "-example"
    )


def test_copy_item_copy_outcome_equal_different_type(
    existent_file_path: Generator[str, None, None],
    non_existent_path: str,
) -> None:
    assert (
        CopyItemCopyOutcome(source=existent_file_path, destination=non_existent_path)
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


# Equal: CommandItemModeChangeOutcome


def test_command_item_run_outcome_equal() -> None:
    assert CommandItemRunOutcome(
        command="true",
    ) == CommandItemRunOutcome(command="true")


def test_command_item_run_outcome_not_equal_path() -> None:
    assert CommandItemRunOutcome(command="true") != CommandItemRunOutcome(
        command="false"
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

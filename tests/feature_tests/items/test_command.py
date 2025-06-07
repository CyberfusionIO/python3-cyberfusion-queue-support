import subprocess

import pytest
from pytest_mock import MockerFixture

from cyberfusion.QueueSupport.exceptions import CommandQueueFulfillFailed
from cyberfusion.QueueSupport.items.command import CommandItem


def test_command_item_fulfill_run(mocker: MockerFixture) -> None:
    spy_run = mocker.spy(subprocess, "run")

    COMMAND = ["echo", "test"]

    object_ = CommandItem(command=COMMAND)
    outcomes = object_.fulfill()

    spy_run.assert_called_once_with(
        COMMAND, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    assert len(outcomes) == 1

    assert COMMAND[1] in outcomes[0].stdout
    assert outcomes[0].stderr is not None


def test_command_item_fulfill_run_failed() -> None:
    COMMAND = ["touch"]

    object_ = CommandItem(command=COMMAND)

    with pytest.raises(CommandQueueFulfillFailed) as e:
        object_.fulfill()

    assert e.value.item == object_
    assert e.value.command == COMMAND
    assert e.value.stdout == ""
    assert "touch" in e.value.stderr  # Exact stderr is platform-dependent
    assert (
        str(e.value)
        == f"Command:\n\n{e.value.command}\n\nStdout:\n\n{e.value.stdout}\n\nStderr:\n\n{e.value.stderr}"
    )

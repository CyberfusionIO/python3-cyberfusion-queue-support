from cyberfusion.QueueSupport.items.command import CommandItem
from cyberfusion.QueueSupport.outcomes import CommandItemRunOutcome
import json
from cyberfusion.QueueSupport.encoders import CustomEncoder

# Equal


def test_command_item_equal() -> None:
    assert CommandItem(command="true") == CommandItem(command="true")


def test_command_item_not_equal_path() -> None:
    assert CommandItem(command="true") != CommandItem(command="false")


def test_command_item_equal_different_type() -> None:
    assert (CommandItem(command="true") == 5) is False


# Outcomes


def test_command_item_has_outcome_run() -> None:
    object_ = CommandItem(command="true")

    assert CommandItemRunOutcome(command="true") in object_.outcomes


# Serialization


def test_command_item_serialization() -> None:
    object_ = CommandItem(command="true")

    serialized = json.dumps(object_, cls=CustomEncoder)
    expected = json.dumps(
        {
            "command": "true",
        }
    )

    assert serialized == expected

import json

import pytest
from cyberfusion.SystemdSupport import Unit

from cyberfusion.QueueSupport.encoders import json_serialize


def test_json_serialize_unit() -> None:
    NAME = "example"

    unit = Unit(name=NAME)

    with pytest.raises(TypeError):
        json.dumps(unit)

    assert (
        json_serialize(
            unit,
        )
        == f'{{"name": "{NAME}"}}'
    )


def test_json_serialize_builtin() -> None:
    WORD = "example"

    assert json.dumps(WORD)

    assert json_serialize(
        WORD,
    )


def test_json_serialize_unsupported() -> None:
    class Class:
        pass

    with pytest.raises(TypeError):
        assert json_serialize(
            Class,
        )

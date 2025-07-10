import json

import pytest

from cyberfusion.QueueSupport.encoders import CustomEncoder
from cyberfusion.QueueSupport.sentinels import UNKNOWN


def test_json_serialize_unknown() -> None:
    with pytest.raises(TypeError):
        json.dumps(UNKNOWN)

    assert json.dumps(UNKNOWN, cls=CustomEncoder) == '"unknown"'


def test_json_serialize_builtin() -> None:
    WORD = "example"

    assert json.dumps(WORD)

    assert json.dumps(WORD, cls=CustomEncoder)


def test_json_serialize_unsupported() -> None:
    class Class:
        pass

    with pytest.raises(TypeError):
        assert json.dumps(Class, cls=CustomEncoder)

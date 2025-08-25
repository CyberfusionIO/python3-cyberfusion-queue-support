from cyberfusion.QueueSupport import make_database_session


def test_make_database_session_engine_uses_custom_encoder() -> None:
    database_session = make_database_session()

    engine = database_session.get_bind()

    assert engine.dialect._json_serializer.__code__.co_names == (
        "json",
        "dumps",
        "CustomEncoder",
    )

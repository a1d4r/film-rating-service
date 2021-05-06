from sqlalchemy.orm import Session

from app.dependencies import get_db


def test_get_db() -> None:
    gen = get_db()
    session = next(gen)
    assert isinstance(session, Session)

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(bind=engine)


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def init_db() -> None:
    from app.models import film, review, user  # noqa

    Base.metadata.create_all(bind=engine)

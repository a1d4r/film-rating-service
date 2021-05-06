from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_repr

from app.database import Base

if TYPE_CHECKING:
    from .review import Review  # noqa


@generic_repr('id', 'login')
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    reviews = relationship('Review', back_populates='user', cascade='all, delete')

    def __str__(self) -> str:
        return str(self.login)

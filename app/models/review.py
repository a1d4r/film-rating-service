from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_repr

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from .film import Film  # noqa
    from .user import User  # noqa


@generic_repr
class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey('film.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    film = relationship('Film', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    @hybrid_property
    def contains_comment(self) -> bool:
        return (self.comment != '') & (self.comment.isnot(None))  # type: ignore

    def __str__(self) -> str:
        return f'{self.user}: {self.rating}'

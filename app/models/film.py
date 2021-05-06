from sqlalchemy import Column, Float, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import aggregated, generic_repr

from app.database import Base
from app.models.review import Review


@generic_repr
class Film(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    reviews = relationship('Review', back_populates='film', cascade='all, delete')

    @aggregated('reviews', Column(Float))
    def rating(self) -> float:
        return func.avg(Review.rating)

    @aggregated('reviews', Column(Integer, default=0))
    def num_reviews(self) -> int:
        return func.sum(Review.contains_comment)

    @aggregated('reviews', Column(Integer, default=0))
    def num_ratings(self) -> int:
        return func.count('*')

    def __str__(self) -> str:
        return str(self.title)

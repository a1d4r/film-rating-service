from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.user import User
from app.schemas.review import (
    ReviewCreateSchema,
    ReviewFullCreateSchema,
    ReviewUpdateSchema,
)

from .base import CRUDBase


class CRUDReview(CRUDBase[Review, ReviewFullCreateSchema, ReviewUpdateSchema]):
    def create_with_user(
        self, db: Session, user: User, review_data: ReviewCreateSchema
    ) -> Review:
        review = Review(**review_data.dict())
        user.reviews.append(review)  # type: ignore
        db.add(review)
        db.commit()
        db.refresh(review)
        return review


review_crud = CRUDReview(Review)

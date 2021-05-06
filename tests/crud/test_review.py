from sqlalchemy.orm import Session

from app.crud.review import review_crud
from app.schemas.review import ReviewCreateSchema, ReviewUpdateSchema
from tests.factories import FilmFactory, ReviewCreateFactory, ReviewFactory, UserFactory


def test_get_review(db: Session):
    actual_review = ReviewFactory()
    retrieved_review = review_crud.get(db, actual_review.id)
    assert retrieved_review == actual_review


def test_get_reviews(db: Session):
    actual_reviews = ReviewFactory.create_batch(3)
    retrieved_reviews = review_crud.get_multi(db)
    assert actual_reviews == retrieved_reviews


def test_create_review(db: Session):
    user = UserFactory()
    film = FilmFactory()
    actual_review_data = ReviewCreateSchema.from_orm(
        ReviewCreateFactory(film_id=film.id)
    )
    review = review_crud.create_with_user(db, user, actual_review_data)
    retrieved_reviewed_data = ReviewCreateSchema.from_orm(review)
    assert actual_review_data == retrieved_reviewed_data
    assert user == review.user


def test_update_review(db: Session):
    review = ReviewFactory()
    db.refresh(review)
    new_review_data = ReviewUpdateSchema.from_orm(ReviewCreateFactory.build())
    updated_review = review_crud.update(db, review, new_review_data)
    retrieved_review_data = ReviewUpdateSchema.from_orm(updated_review)
    assert new_review_data == retrieved_review_data


def test_delete_review(db: Session):
    review = ReviewFactory()
    deleted_review = review_crud.remove(db, review.id)
    retrieved_review = review_crud.get(db, review.id)
    assert review == deleted_review
    assert retrieved_review is None
